#-------------------------------------------------------------------------------
#
# Project: EOxServer <http://eoxserver.org>
# Authors: Fabian Schindler <fabian.schindler@eox.at>
#          Stephan Meissl <stephan.meissl@eox.at>
#          Stephan Krause <stephan.krause@eox.at>
#
#-------------------------------------------------------------------------------
# Copyright (C) 2011 EOX IT Services GmbH
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
#-------------------------------------------------------------------------------

from django.core.exceptions import ValidationError, MultipleObjectsReturned
from django.contrib.gis import forms
from django.contrib.gis import admin
from django.contrib import messages
from django.urls import reverse

# from eoxserver.contrib import gdal
# from eoxserver.backends import models as backends
from eoxserver.resources.coverages import models
from eoxserver.resources.coverages import views
# from eoxserver.backends.admin import LocationForm

# ==============================================================================
# Inline "Type" model admins
# ==============================================================================


class FieldTypeInline(admin.StackedInline):
    model = models.FieldType
    filter_horizontal = ['nil_values']
    extra = 0

    def get_queryset(self, *args, **kwargs):
        queryset = super(FieldTypeInline, self).get_queryset(*args, **kwargs)
        return queryset.order_by("index")


class MaskTypeInline(admin.TabularInline):
    model = models.MaskType
    extra = 0


# ==============================================================================
# Inline admins
# ==============================================================================

class MaskInline(admin.StackedInline):
    model = models.Mask
    extra = 0


class BrowseInline(admin.StackedInline):
    model = models.Browse
    extra = 0

    # fields = ( 'image_tag', )
    readonly_fields = ('browse_image_tag',)

    def browse_image_tag(self, obj):
        return u'<img src="%s" />' % reverse(
            views.browse_view, kwargs={'identifier': obj.product.identifier}
        )

    browse_image_tag.short_description = 'Image'
    browse_image_tag.allow_tags = True
    browse_image_tag.empty_value_display = ''


class CoverageMetadataInline(admin.StackedInline):
    model = models.CoverageMetadata
    extra = 0


class ProductMetadataInline(admin.StackedInline):
    model = models.ProductMetadata
    extra = 0


class CollectionMetadataInline(admin.StackedInline):
    model = models.CollectionMetadata
    extra = 0


# ==============================================================================
# Abstract admins
# ==============================================================================

class EOObjectAdmin(admin.ModelAdmin):
    pass

# ==============================================================================
# "Type" model admins
# ==============================================================================


class CoverageTypeAdmin(admin.ModelAdmin):
    inlines = [FieldTypeInline]

admin.site.register(models.CoverageType, CoverageTypeAdmin)


class ProductTypeAdmin(admin.ModelAdmin):
    inlines = [MaskTypeInline]
    filter_horizontal = ['allowed_coverage_types']

admin.site.register(models.ProductType, ProductTypeAdmin)


class CollectionTypeAdmin(admin.ModelAdmin):
    filter_horizontal = ['allowed_product_types', 'allowed_coverage_types']

admin.site.register(models.CollectionType, CollectionTypeAdmin)


class MaskTypeAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.MaskType, MaskTypeAdmin)


class BrowseTypeAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.BrowseType, BrowseTypeAdmin)


class GridAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.Grid, GridAdmin)

# ==============================================================================
# Collection, Product and Coverage admins
# ==============================================================================


class CoverageAdmin(EOObjectAdmin):
    inlines = [CoverageMetadataInline]

admin.site.register(models.Coverage, CoverageAdmin)


class ProductAdmin(EOObjectAdmin):
    inlines = [MaskInline, BrowseInline, ProductMetadataInline]

admin.site.register(models.Product, ProductAdmin)


class CollectionAdmin(EOObjectAdmin):
    inlines = [CollectionMetadataInline]

    actions = ['summary']

    # action to refresh the summary info on a collection
    def summary(self, request, queryset):
        for collection in queryset:
            models.collection_collect_metadata(
                collection, product_summary=True, coverage_summary=True
            )

    summary.short_description = (
        "Update the summary information for each collection"
    )

admin.site.register(models.Collection, CollectionAdmin)


class IndexHiddenAdmin(admin.ModelAdmin):
    """ Admin class that hides on the apps admin index page.
        """
    def get_model_perms(self, request):
        return {}

admin.site.register(models.OrbitNumber, IndexHiddenAdmin)
admin.site.register(models.Track, IndexHiddenAdmin)
admin.site.register(models.Frame, IndexHiddenAdmin)
admin.site.register(models.SwathIdentifier, IndexHiddenAdmin)
admin.site.register(models.ProductVersion, IndexHiddenAdmin)
admin.site.register(models.ProductQualityDegredationTag, IndexHiddenAdmin)
admin.site.register(models.ProcessorName, IndexHiddenAdmin)
admin.site.register(models.ProcessingCenter, IndexHiddenAdmin)
admin.site.register(models.SensorMode, IndexHiddenAdmin)
admin.site.register(models.ArchivingCenter, IndexHiddenAdmin)
admin.site.register(models.ProcessingMode, IndexHiddenAdmin)
admin.site.register(models.AcquisitionStation, IndexHiddenAdmin)
admin.site.register(models.AcquisitionSubType, IndexHiddenAdmin)
