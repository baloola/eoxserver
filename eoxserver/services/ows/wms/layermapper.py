# ------------------------------------------------------------------------------
#
# Project: EOxServer <http://eoxserver.org>
# Authors: Fabian Schindler <fabian.schindler@eox.at>
#
# ------------------------------------------------------------------------------
# Copyright (C) 2017 EOX IT Services GmbH
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies of this Software or works derived from this Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
# ------------------------------------------------------------------------------

from eoxserver.core.util.timetools import isoformat
from eoxserver.render.map.objects import (
    CoverageLayer, MosaicLayer, OutlinesLayer, BrowseLayer, OutlinedBrowseLayer,
    MaskLayer, MaskedBrowseLayer,
    LayerDescription,
)
from eoxserver.render.coverage.objects import Coverage as RenderCoverage
from eoxserver.render.coverage.objects import Mosaic as RenderMosaic
from eoxserver.render.browse.objects import (
    Browse, GeneratedBrowse, Mask, MaskedBrowse
)
from eoxserver.resources.coverages import models


class UnsupportedObject(Exception):
    pass


class NoSuchLayer(Exception):
    pass


class NoSuchPrefix(NoSuchLayer):
    pass


class LayerMapper(object):
    """ Default layer mapper.
    """

    def __init__(self, supported_layer_types, suffix_separator):
        self.supported_layer_types = supported_layer_types
        self.suffix_separator = suffix_separator

    def get_layer_description(self, eo_object, raster_styles, geometry_styles):
        if isinstance(eo_object, models.Coverage):
            coverage = RenderCoverage.from_model(eo_object)
            return LayerDescription.from_coverage(coverage, raster_styles)
        elif isinstance(eo_object, models.Mosaic):
            coverage = RenderCoverage.from_model(eo_object)
            return LayerDescription.from_mosaic(coverage, raster_styles)
        elif isinstance(eo_object, (models.Product, models.Collection)):
            mask_types = []
            browse_types = []
            if getattr(eo_object, "product_type", None):
                browse_types = eo_object.product_type.browse_types.all()
                mask_types = eo_object.product_type.mask_types.all()
            elif getattr(eo_object, "collection_type", None):
                browse_types = models.BrowseType.objects.filter(
                    product_type__allowed_collection_types__collections=eo_object
                )
                mask_types = models.MaskType.objects.filter(
                    product_type__allowed_collection_types__collections=eo_object
                )

            sub_layers = [
                LayerDescription(
                    "%s%soutlines" % (
                        eo_object.identifier, self.suffix_separator
                    ),
                    styles=geometry_styles,
                    queryable=True
                ),
                LayerDescription(
                    "%s%soutlined" % (
                        eo_object.identifier, self.suffix_separator
                    ),
                    styles=geometry_styles,
                    queryable=True
                )
            ]
            for browse_type in browse_types:
                sub_layers.append(
                    LayerDescription(
                        "%s%s%s" % (
                            eo_object.identifier, self.suffix_separator,
                            browse_type.name
                        ),
                        styles=geometry_styles
                    )
                )

            for mask_type in mask_types:
                sub_layers.append(
                    LayerDescription(
                        "%s%s%s" % (
                            eo_object.identifier, self.suffix_separator,
                            mask_type.name
                        ),
                        styles=geometry_styles
                    )
                )
                sub_layers.append(
                    LayerDescription(
                        "%s%smasked_%s" % (
                            eo_object.identifier, self.suffix_separator,
                            mask_type.name
                        ),
                        styles=geometry_styles
                    )
                )

            dimensions = {}
            if eo_object.begin_time and eo_object.end_time:
                dimensions["time"] = {
                    'min': isoformat(eo_object.begin_time),
                    'max': isoformat(eo_object.end_time),
                    'step': 'PT1S',
                    'default': isoformat(eo_object.end_time),
                    'units': 'ISO8601'
                }

            return LayerDescription(
                name=eo_object.identifier,
                bbox=eo_object.footprint.extent if eo_object.footprint else None,
                dimensions=dimensions,
                sub_layers=sub_layers
            )

        raise UnsupportedObject(
            "Object %r cannot be mapped to a layer." % eo_object
        )

    def lookup_layer(self, layer_name, suffix, style, filters_expressions,
                     sort_by, time, range, bands, wavelengths, elevation):
        """ Lookup the layer from the registered objects.
        """
        full_name = '%s%s%s' % (layer_name, self.suffix_separator, suffix)

        try:
            eo_object = models.EOObject.objects.select_subclasses(
                models.Collection, models.Product, models.Coverage,
                models.Mosaic
            ).get(
                identifier=layer_name
            )
        except models.EOObject.DoesNotExist:
            raise NoSuchLayer('Layer %r does not exist' % layer_name)

        if isinstance(eo_object, models.Coverage):
            if suffix not in ('', 'bands'):
                raise NoSuchLayer('Invalid layer suffix %r' % suffix)
            return CoverageLayer(
                full_name, style,
                RenderCoverage.from_model(eo_object),
                bands, wavelengths, time, elevation, range
            )

        # TODO: deprecated
        elif isinstance(eo_object, models.Mosaic):
            return MosaicLayer(
                full_name, style,
                RenderMosaic.from_model(eo_object), [
                    RenderCoverage.from_model(coverage)
                    for coverage in self.iter_coverages(
                        eo_object, filters_expressions, sort_by
                    )
                ], bands, wavelengths, time, elevation, range
            )

        elif isinstance(eo_object, (models.Collection, models.Product)):
            if suffix == '' or suffix == 'outlined':
                browses = []
                product_browses = self.iter_products_browses(
                    eo_object, filters_expressions, sort_by, None, style
                )

                for product, browse in product_browses:
                    # When bands/wavelengths are specifically requested, make a
                    # generated browse
                    if bands or wavelengths:
                        browses.append(
                            _generate_browse_from_bands(
                                product, bands, wavelengths
                            )
                        )

                    # When available use the default browse
                    elif browse:
                        browses.append(Browse.from_model(product, browse))

                    # As fallback use the default browse type (with empty name)
                    # to generate a browse from the specified bands
                    else:
                        browse_type = product.product_type.browse_types.filter(
                            name=''
                        ).first()
                        if browse_type:
                            browses.append(
                                _generate_browse_from_browse_type(
                                    product, browse_type
                                )
                            )

                # either return the simple browse layer or the outlined one
                if suffix == '':
                    return BrowseLayer(
                        name=full_name, style=style,
                        browses=browses, range=range
                    )
                else:
                    return OutlinedBrowseLayer(
                        name=full_name, style=style,
                        browses=browses, range=range
                    )

            elif suffix == 'outlines':
                return OutlinesLayer(
                    name=full_name, style=style,
                    footprints=[
                        product.footprint for product in self.iter_products(
                            eo_object, filters_expressions, sort_by,
                        )
                    ]
                )

            elif suffix.startswith('masked_'):
                post_suffix = suffix[len('masked_'):]
                mask_type = self.get_mask_type(eo_object, post_suffix)

                if not mask_type:
                    raise NoSuchLayer('No such mask type %r' % post_suffix)

                masked_browses = []

                product_browses_mask = self.iter_products_browses_masks(
                    eo_object, filters_expressions, sort_by, post_suffix
                )
                for product, browse, mask in product_browses_mask:
                    # When bands/wavelengths are specifically requested, make a
                    # generated browse
                    if bands or wavelengths:
                        masked_browses.append(
                            MaskedBrowse(
                                browse=_generate_browse_from_bands(
                                    product, bands, wavelengths
                                ),
                                mask=Mask.from_model(mask)
                            )
                        )

                    # When available use the default browse
                    elif browse:
                        masked_browses.append(
                            MaskedBrowse.from_model(product, browse, mask)
                        )

                    # As fallback use the default browse type (with empty name)
                    # to generate a browse from the specified bands
                    else:
                        browse_type = product.product_type.browse_types.filter(
                            name=''
                        ).first()
                        if browse_type:
                            masked_browses.append(
                                MaskedBrowse(
                                    browse=_generate_browse_from_browse_type(
                                        product, browse_type
                                    ),
                                    mask=Mask.from_model(mask)
                                )
                            )

                return MaskedBrowseLayer(
                    name=full_name, style=style,
                    masked_browses=[
                        MaskedBrowse.from_models(product, browse, mask)
                        for product, browse, mask in
                        self.iter_products_browses_masks(
                            eo_object, filters_expressions, sort_by, post_suffix
                        )
                    ]
                )

            else:
                # either browse type or mask type
                browse_type = self.get_browse_type(eo_object, suffix)
                if browse_type:
                    browses = []

                    product_browses = self.iter_products_browses(
                        eo_object, filters_expressions, sort_by, suffix,
                        style
                    )

                    for product, browse in product_browses:
                        # check if a browse is already available for that
                        # browse type.
                        if browse:
                            browses.append(Browse.from_model(product, browse))

                        # if no browse is available for that browse type,
                        # generate a new browse with the instructions of that
                        # browse type
                        else:
                            browses.append(
                                _generate_browse_from_browse_type(
                                    product, browse_type
                                )
                            )

                    return BrowseLayer(
                        name=full_name, style=style, range=range,
                        browses=browses
                    )

                mask_type = self.get_mask_type(eo_object, suffix)
                if mask_type:
                    return MaskLayer(
                        name=full_name, style=style,
                        masks=[
                            Mask.from_model(mask_model)
                            for _, mask_model in self.iter_products_masks(
                                eo_object, filters_expressions, sort_by, suffix
                            )
                        ]
                    )

                raise NoSuchLayer('Invalid layer suffix %r' % suffix)

    def split_layer_suffix_name(self, layer_name):
        return layer_name.partition(self.suffix_separator)[::2]

    def get_browse_type(self, eo_object, name):
        if isinstance(eo_object, models.Product):
            filter_ = dict(product_type__products=eo_object)
        else:
            filter_ = dict(
                product_type__allowed_collection_types__collections=eo_object
            )

        return models.BrowseType.objects.filter(name=name, **filter_).first()

    def get_mask_type(self, eo_object, name):
        if isinstance(eo_object, models.Product):
            filter_ = dict(product_type__products=eo_object)
        else:
            filter_ = dict(
                product_type__allowed_collection_types__collections=eo_object
            )

        return models.MaskType.objects.filter(name=name, **filter_).first()

    #
    # iteration methods
    #

    def iter_coverages(self, eo_object, filters_expressions, sort_by=None):
        if isinstance(eo_object, models.Mosaic):
            base_filter = dict(mosaics=eo_object)
        else:
            pass  # TODO

        qs = models.Coverage.objects.filter(filters_expressions, **base_filter)
        if sort_by:
            qs = qs.order_by('%s%s' % (
                '-' if sort_by[1] == 'DESC' else '',
                sort_by[0]
            ))

        return qs

    def iter_products(self, eo_object, filters_expressions, sort_by=None):
        if isinstance(eo_object, models.Collection):
            base_filter = dict(collections=eo_object)
        else:
            base_filter = dict(pk=eo_object.pk)

        qs = models.Product.objects.filter(filters_expressions, **base_filter)

        if sort_by:
            qs = qs.order_by('%s%s' % (
                '-' if sort_by[1] == 'DESC' else '',
                sort_by[0]
            ))

        return qs

    def iter_products_browses(self, eo_object, filters_expressions, sort_by,
                              name=None, style=None):
        products = self.iter_products(
            eo_object, filters_expressions, sort_by
        ).prefetch_related('browses')

        for product in products:
            browses = product.browses
            if name:
                browses = browses.filter(browse_type__name=name)
            else:
                browses = browses.filter(browse_type__isnull=True)

            # if style:
            #     browses = browses.filter(style=style)
            # else:
            #     browses = browses.filter(style__isnull=True)

            yield (product, browses.first())

    def iter_products_masks(self, eo_object, filters_expressions, sort_by,
                            name=None):
        products = self.iter_products(
            eo_object, filters_expressions, sort_by
        ).prefetch_related('masks')

        for product in products:
            masks = product.masks
            if name:
                mask = masks.filter(mask_type__name=name).first()
            else:
                mask = masks.filter(mask_type__isnull=True).first()

            yield (product, mask)

    def iter_products_browses_masks(self, eo_object, filters_expressions,
                                    sort_by, name=None):
        products = self.iter_products(
            eo_object, filters_expressions, sort_by
        ).prefetch_related('masks', 'browses')

        for product in products:
            if name:
                mask = product.masks.filter(mask_type__name=name).first()
            else:
                mask = product.masks.filter(mask_type__isnull=True).first()

            browse = product.browses.filter(browse_type__isnull=True).first()

            yield (product, browse, mask)


def _generate_browse_from_browse_type(product, browse_type):
    fields_and_coverages = [
        (
            browse_type.red_or_grey_expression,
            product.coverages.filter(
                coverage_type__field_types__identifier=browse_type.red_or_grey_expression
            )
        )
    ]
    if browse_type.green_expression and browse_type.blue_expression:
        fields_and_coverages.append((
            browse_type.green_expression,
            product.coverages.filter(
                coverage_type__field_types__identifier=browse_type.green_expression
            )
        ))
        fields_and_coverages.append((
            browse_type.blue_expression,
            product.coverages.filter(
                coverage_type__field_types__identifier=browse_type.blue_expression
            )
        ))
        if browse_type.alpha_expression:
            fields_and_coverages.append((
                browse_type.alpha_expression,
                product.coverages.filter(
                    coverage_type__field_types__identifier=browse_type.alpha_expression
                )
            ))
    return GeneratedBrowse.from_coverage_models(
        fields_and_coverages, product
    )


def _generate_browse_from_bands(product, bands, wavelengths):
    assert len(bands or wavelengths or []) in (1, 3, 4)

    if bands:
        fields_and_coverages = [
            (
                band_name,
                product.coverages.filter(
                    coverage_type__field_types__identifier=band_name
                )
            )
            for band_name in bands
        ]
    elif wavelengths:
        fields_and_coverages = [
            (
                product.coverages.filter(
                    coverage_type__field_types__wavelength=wavelength
                ).first().name,
                product.coverages.filter(
                    coverage_type__field_types__wavelength=wavelength
                )
            )
            for wavelength in wavelengths
        ]

    return GeneratedBrowse.from_coverage_models(
        fields_and_coverages, product
    )
