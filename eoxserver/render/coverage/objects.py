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

from itertools import izip_longest

from eoxserver.core.util.timetools import parse_iso8601, parse_duration
from eoxserver.contrib import gdal
from eoxserver.contrib.osr import SpatialReference
from eoxserver.backends.access import get_vsi_path

GRID_TYPE_ELEVATION = 1
GRID_TYPE_TEMPORAL = 2


def is_referenceable(grid_model):
    return grid_model.axis_1_offset is None


class Field(object):
    def __init__(self, index, identifier, description, definition,
                 unit_of_measure, wavelength, significant_figures,
                 allowed_values, nil_values, data_type, data_type_range):
        self._index = index
        self._identifier = identifier
        self._description = description
        self._definition = definition
        self._unit_of_measure = unit_of_measure
        self._wavelength = wavelength
        self._significant_figures = significant_figures
        self._allowed_values = allowed_values
        self._nil_values = nil_values
        self._data_type = data_type
        self._data_type_range = data_type_range

    @property
    def index(self):
        return self._index

    @property
    def identifier(self):
        return self._identifier

    @property
    def description(self):
        return self._description

    @property
    def definition(self):
        return self._definition

    @property
    def unit_of_measure(self):
        return self._unit_of_measure

    @property
    def wavelength(self):
        return self._wavelength

    @property
    def significant_figures(self):
        return self._significant_figures

    @property
    def allowed_values(self):
        return self._allowed_values

    @property
    def nil_values(self):
        return self._nil_values

    @property
    def data_type(self):
        return self._data_type

    @property
    def data_type_range(self):
        return self._data_type_range

    def __eq__(self, other):
        try:
            return (
                self._identifier == other._identifier and
                self._description == other._description and
                self._definition == other._definition and
                self._unit_of_measure == other._unit_of_measure and
                self._wavelength == other._wavelength and
                self._significant_figures == other._significant_figures and
                self._allowed_values == other._allowed_values and
                self._nil_values == other._nil_values and
                self._data_type == other._data_type and
                self._data_type_range == other._data_type_range
            )
        except AttributeError:
            return False


class RangeType(list):
    def __init__(self, name, fields):
        super(RangeType, self).__init__(fields)
        self._name = name

    @property
    def name(self):
        return self._name

    @classmethod
    def from_coverage_type(cls, coverage_type):
        def get_data_type(field_type):
            numbits = (
                field_type.numbits if field_type.numbits is not None else 32
            )
            signed = field_type.signed
            is_float = field_type.is_float

            if is_float:
                if numbits <= 32:
                    return gdal.GDT_Float32
                return gdal.GDT_Float64
            elif signed:
                if numbits <= 8:
                    return gdal.GDT_Byte
                elif numbits <= 16:
                    return gdal.GDT_Int16
                else:
                    return gdal.GDT_Int32
            else:
                if numbits <= 8:
                    return gdal.GDT_Byte
                elif numbits <= 16:
                    return gdal.GDT_UInt16
                else:
                    return gdal.GDT_UInt32
            return gdal.GDT_Unknown

        def get_data_type_range(field_type):
            numbits = (
                field_type.numbits if field_type.numbits is not None else 32
            )
            signed = field_type.signed
            is_float = field_type.is_float
            if is_float:
                if numbits == 32:
                    return gdal.GDT_NUMERIC_LIMITS[gdal.GDT_Float32]
                elif numbits == 64:
                    return gdal.GDT_NUMERIC_LIMITS[gdal.GDT_Float64]
            elif signed:
                max_ = 2 ** (numbits - 1)
                return (-max_, max_ - 1)
            else:
                return (0, 2 ** numbits)

        return cls(coverage_type.name, [
            Field(
                index=i,
                identifier=field_type.identifier,
                description=field_type.description,
                definition=field_type.definition,
                unit_of_measure=field_type.unit_of_measure,
                wavelength=field_type.wavelength,
                significant_figures=field_type.significant_figures,
                allowed_values=[
                    (value_range.start, value_range.end)
                    for value_range in field_type.allowed_value_ranges.all()
                ],
                nil_values=[
                    (nil_value.value, nil_value.reason)
                    for nil_value in field_type.nil_values.all()
                ],
                data_type=get_data_type(field_type),
                data_type_range=get_data_type_range(field_type)
            )
            for i, field_type in enumerate(coverage_type.field_types.all())
        ])

    @classmethod
    def from_gdal_dataset(cls, ds, base_identifier):
        fields = []
        bandoffset = 0
        for i in range(ds.RasterCount):
            band = ds.GetRasterBand(i + 1)
            nodata_value = band.GetNoDataValue()
            if nodata_value is not None:
                nil_values = [(nodata_value, "")]
            else:
                nil_values = []

            fields.append(
                Field(
                    index=i,
                    identifier="%s_%d" % (base_identifier, bandoffset + i),
                    # TODO: get info from band metadata?
                    description="",
                    definition="",
                    unit_of_measure="",
                    wavelength="",
                    significant_figures=gdal.GDT_SIGNIFICANT_FIGURES.get(
                        band.DataType
                    ),
                    allowed_values=[
                        gdal.GDT_NUMERIC_LIMITS[band.DataType]
                    ]
                    if band.DataType in gdal.GDT_NUMERIC_LIMITS else [],
                    nil_values=nil_values,
                    data_type=band.DataType,
                    data_type_range=gdal.GDT_NUMERIC_LIMITS.get(band.DataType)
                )
            )
            bandoffset += 1
        return cls(base_identifier, fields)


class Axis(object):
    def __init__(self, name, type, offset):
        self._name = name
        self._type = type
        self._offset = offset

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self._type

    @property
    def offset(self):
        return self._offset


class Grid(list):
    def __init__(self, coordinate_reference_system, axes):
        super(Grid, self).__init__(axes)
        self._coordinate_reference_system = coordinate_reference_system

    @classmethod
    def from_model(cls, grid_model):
        is_ref = is_referenceable(grid_model)
        names = grid_model.axis_names
        types = grid_model.axis_types
        offsets = grid_model.axis_offsets

        axes = []

        axes_iter = izip_longest(names, types, offsets)
        for name, type_, offset in axes_iter:
            if is_ref:
                offset = None
            elif type_ == GRID_TYPE_TEMPORAL:
                offset = parse_duration(offset)
            else:
                offset = float(offset)

            axes.append(Axis(name, type_, offset))

        return cls(grid_model.coordinate_reference_system, axes)

    @property
    def spatial_reference(self):
        return SpatialReference(self.coordinate_reference_system)

    @property
    def coordinate_reference_system(self):
        return self._coordinate_reference_system

    @property
    def names(self):
        return [axis.name for axis in self]

    @property
    def types(self):
        return [axis.type for axis in self]

    @property
    def offsets(self):
        return [axis.offset for axis in self]

    @property
    def has_elevation(self):
        return GRID_TYPE_ELEVATION in self.types

    @property
    def has_temporal(self):
        return GRID_TYPE_TEMPORAL in self.types

    @property
    def is_referenceable(self):
        return self[0].offset is None


class Origin(list):
    @classmethod
    def from_description(cls, axis_types, origins):
        return cls([
            parse_iso8601(orig) if type_ == GRID_TYPE_TEMPORAL else float(orig)
            for type_, orig in zip(axis_types, origins)
        ])


class EOMetadata(object):
    def __init__(self, begin_time, end_time, footprint):
        self._begin_time = begin_time
        self._end_time = end_time
        self._footprint = footprint

    @property
    def footprint(self):
        return self._footprint

    @property
    def begin_time(self):
        return self._begin_time

    @property
    def end_time(self):
        return self._end_time


class Location(object):
    def __init__(self, path, format):
        self._path = path
        self._format = format

    @property
    def path(self):
        return self._path

    @property
    def format(self):
        return self._format


class ArraydataLocation(Location):
    def __init__(self, path, format, start_field, end_field):
        super(ArraydataLocation, self).__init__(path, format)
        self._start_field = start_field
        self._end_field = end_field

    @property
    def start_field(self):
        return self._start_field

    @property
    def end_field(self):
        return self._end_field

    def field_index_to_band_index(self, field_index):
        return field_index - self.start_field


class Coverage(object):
    """ Representation of a coverage for internal processing.
    """
    def __init__(self, identifier, eo_metadata, range_type, grid, origin, size,
                 arraydata_locations, metadata_locations):
        self._identifier = identifier
        self._eo_metadata = eo_metadata
        self._range_type = range_type
        self._origin = origin
        self._grid = grid
        self._size = size
        self._arraydata_locations = arraydata_locations
        self._metadata_locations = metadata_locations

    @property
    def identifier(self):
        return self._identifier

    @property
    def eo_metadata(self):
        return self._eo_metadata

    @property
    def footprint(self):
        return self._eo_metadata.footprint if self._eo_metadata else None

    @property
    def begin_time(self):
        return self._eo_metadata.begin_time if self._eo_metadata else None

    @property
    def end_time(self):
        return self._eo_metadata.end_time if self._eo_metadata else None

    @property
    def range_type(self):
        return self._range_type

    @property
    def origin(self):
        return self._origin

    @property
    def grid(self):
        return self._grid

    @property
    def size(self):
        return tuple(self._size)

    @property
    def arraydata_locations(self):
        return self._arraydata_locations

    @property
    def metadata_locations(self):
        return self._metadata_locations

    @property
    def coverage_subtype(self):
        subtype = "RectifiedDataset"
        if not self.footprint or not self.begin_time or not self.end_time:
            subtype = "RectifiedGridCoverage"
        elif self.grid.is_referenceable:
            subtype = "ReferenceableDataset"
        return subtype

    @property
    def extent(self):
        types = self.grid.types
        offsets = self.grid.offsets

        lows = []
        highs = []

        axes = izip_longest(types, offsets, self.origin, self.size)
        for type_, offset, origin, size in axes:
            a = origin
            b = origin + size * offset

            if offset > 0:
                lows.append(a)
                highs.append(b)
            else:
                lows.append(b)
                highs.append(a)

        return tuple(lows + highs)

    def get_location_for_field(self, field_or_identifier):
        if isinstance(field_or_identifier, Field):
            field = field_or_identifier
            if field not in self.range_type:
                return None
        else:
            try:
                field = next(
                    field
                    for field in self.range_type
                    if field.identifier == field_or_identifier
                )
            except StopIteration:
                return None

        index = field.index
        for location in self.arraydata_locations:
            if index >= location.start_field and index <= location.end_field:
                return location

    def get_band_index_for_field(self, field_or_identifier):
        if isinstance(field_or_identifier, Field):
            field = field_or_identifier
            if field not in self.range_type:
                return None
        else:
            try:
                field = next(
                    field
                    for field in self.range_type
                    if field.identifier == field_or_identifier
                )
            except StopIteration:
                return None

        index = field.index
        for location in self.arraydata_locations:
            if index >= location.start_field and index <= location.end_field:
                return index - location.start_field + 1

    @classmethod
    def from_model(cls, coverage_model):
        eo_metadata = EOMetadata(None, None, None)
        if coverage_model.begin_time and coverage_model.end_time and \
                coverage_model.footprint:
            eo_metadata = EOMetadata(
                coverage_model.begin_time, coverage_model.end_time,
                coverage_model.footprint
            )
        elif coverage_model.parent_product:
            product = coverage_model.parent_product
            if product.begin_time and product.end_time and product.footprint:
                eo_metadata = EOMetadata(
                    coverage_model.begin_time, coverage_model.end_time,
                    coverage_model.footprint
                )

        arraydata_locations = [
            ArraydataLocation(
                get_vsi_path(item), item.format,
                item.field_index, item.field_index + (item.band_count - 1)
            )
            for item in coverage_model.arraydata_items.all()
        ]

        metadata_locations = [
            Location(get_vsi_path(item), item.format)
            for item in coverage_model.metadata_items.all()
        ]

        if coverage_model.coverage_type:
            range_type = RangeType.from_coverage_type(
                coverage_model.coverage_type
            )
        else:
            range_type = RangeType.from_gdal_dataset(
                gdal.OpenShared(arraydata_locations[0].path),
                coverage_model.identifier
            )

        grid = Grid.from_model(coverage_model.grid)

        origin = Origin.from_description(grid.types, coverage_model.origin)

        return cls(
            identifier=coverage_model.identifier,
            eo_metadata=eo_metadata, range_type=range_type, origin=origin,
            grid=grid, size=coverage_model.size,
            arraydata_locations=arraydata_locations,
            metadata_locations=metadata_locations
        )


class Mosaic(object):
    def __init__(self, identifier, eo_metadata, range_type, grid, origin, size):
        self._identifier = identifier
        self._eo_metadata = eo_metadata
        self._range_type = range_type
        self._origin = origin
        self._grid = grid
        self._size = size

    @property
    def identifier(self):
        return self._identifier

    @property
    def eo_metadata(self):
        return self._eo_metadata

    @property
    def footprint(self):
        return self._eo_metadata.footprint if self._eo_metadata else None

    @property
    def begin_time(self):
        return self._eo_metadata.begin_time if self._eo_metadata else None

    @property
    def end_time(self):
        return self._eo_metadata.end_time if self._eo_metadata else None

    @property
    def range_type(self):
        return self._range_type

    @property
    def origin(self):
        return self._origin

    @property
    def grid(self):
        return self._grid

    @property
    def size(self):
        return tuple(self._size)

    # @property
    # def coverage_subtype(self):
    #     subtype = "DatasetSeries"
    #     if not self.footprint or not self.begin_time or not self.end_time:
    #         subtype = "RectifiedStitchedMosaic"
    #     elif self.grid.is_referenceable:
    #         subtype = "ReferenceableStitchedMosaic"
    #     return subtype

    @property
    def extent(self):
        if not self.grid:
            return None

        types = self.grid.types
        offsets = self.grid.offsets

        lows = []
        highs = []

        axes = izip_longest(types, offsets, self.origin, self.size)
        for type_, offset, origin, size in axes:
            a = origin
            b = origin + size * offset

            if offset > 0:
                lows.append(a)
                highs.append(b)
            else:
                lows.append(b)
                highs.append(a)

        return tuple(lows + highs)

    @classmethod
    def from_model(cls, mosaic_model):
        eo_metadata = EOMetadata(None, None, None)
        if mosaic_model.begin_time and mosaic_model.end_time and \
                mosaic_model.footprint:
            eo_metadata = EOMetadata(
                mosaic_model.begin_time, mosaic_model.end_time,
                mosaic_model.footprint
            )

        range_type = RangeType.from_coverage_type(
            mosaic_model.coverage_type
        )

        grid_model = mosaic_model.grid
        grid = None
        origin = None
        if grid_model:
            grid = Grid.from_model(grid_model)
            origin = Origin.from_description(grid.types, mosaic_model.origin)

        return cls(
            identifier=mosaic_model.identifier,
            eo_metadata=eo_metadata, range_type=range_type, origin=origin,
            grid=grid, size=mosaic_model.size,
        )
