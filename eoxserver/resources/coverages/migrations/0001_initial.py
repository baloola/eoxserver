# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-07 08:32
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import re


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('backends', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AcquisitionStation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(db_index=True, max_length=256, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AcquisitionSubType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(db_index=True, max_length=256, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AllowedValueRange',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.FloatField()),
                ('end', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='ArchivingCenter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(db_index=True, max_length=256, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ArrayDataItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=1024)),
                ('format', models.CharField(blank=True, max_length=64, null=True)),
                ('field_index', models.PositiveSmallIntegerField(default=0)),
                ('band_count', models.PositiveSmallIntegerField(default=1)),
                ('subdataset_type', models.CharField(blank=True, max_length=64, null=True)),
                ('subdataset_locator', models.CharField(blank=True, max_length=1024, null=True)),
                ('bands_interpretation', models.PositiveSmallIntegerField(choices=[(0, b'fields'), (1, b'dimension')], default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Browse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=1024)),
                ('format', models.CharField(blank=True, max_length=64, null=True)),
                ('style', models.CharField(blank=True, max_length=256, null=True)),
                ('coordinate_reference_system', models.TextField()),
                ('min_x', models.FloatField()),
                ('min_y', models.FloatField()),
                ('max_x', models.FloatField()),
                ('max_y', models.FloatField()),
                ('width', models.PositiveIntegerField()),
                ('height', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='BrowseType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, validators=[django.core.validators.RegexValidator(re.compile(b'^[a-zA-z_][a-zA-Z0-9_]*$'), message=b'This field must contain a valid Name.')])),
                ('red_or_grey_expression', models.CharField(blank=True, max_length=512, null=True)),
                ('green_expression', models.CharField(blank=True, max_length=512, null=True)),
                ('blue_expression', models.CharField(blank=True, max_length=512, null=True)),
                ('alpha_expression', models.CharField(blank=True, max_length=512, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CollectionMetadata',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_type', models.CharField(blank=True, db_index=True, max_length=256, null=True)),
                ('doi', models.CharField(blank=True, db_index=True, max_length=256, null=True)),
                ('platform', models.CharField(blank=True, db_index=True, max_length=256, null=True)),
                ('platform_serial_identifier', models.CharField(blank=True, db_index=True, max_length=256, null=True)),
                ('instrument', models.CharField(blank=True, db_index=True, max_length=256, null=True)),
                ('sensor_type', models.CharField(blank=True, db_index=True, max_length=256, null=True)),
                ('composite_type', models.CharField(blank=True, db_index=True, max_length=256, null=True)),
                ('processing_level', models.CharField(blank=True, db_index=True, max_length=256, null=True)),
                ('orbit_type', models.CharField(blank=True, db_index=True, max_length=256, null=True)),
                ('spectral_range', models.CharField(blank=True, db_index=True, max_length=256, null=True)),
                ('wavelength', models.IntegerField(blank=True, db_index=True, null=True)),
                ('product_metadata_summary', models.TextField(blank=True, null=True)),
                ('coverage_metadata_summary', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CollectionType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=512, unique=True, validators=[django.core.validators.RegexValidator(re.compile(b'^[a-zA-z_][a-zA-Z0-9_]*$'), message=b'This field must contain a valid Name.')])),
            ],
        ),
        migrations.CreateModel(
            name='CoverageMetadata',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='CoverageType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=512, unique=True, validators=[django.core.validators.RegexValidator(re.compile(b'^[a-zA-z_][a-zA-Z0-9_]*$'), message=b'This field must contain a valid Name.')])),
            ],
        ),
        migrations.CreateModel(
            name='EOObject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(max_length=256, unique=True, validators=[django.core.validators.RegexValidator(re.compile(b'^[a-zA-z_][a-zA-Z0-9_.-]*$'), message=b'This field must contain a valid NCName.')])),
                ('begin_time', models.DateTimeField(blank=True, null=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('footprint', django.contrib.gis.db.models.fields.GeometryField(blank=True, null=True, srid=4326)),
                ('inserted', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='FieldType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.PositiveSmallIntegerField()),
                ('identifier', models.CharField(max_length=512, validators=[django.core.validators.RegexValidator(re.compile(b'^[a-zA-z_][a-zA-Z0-9_.-]*$'), message=b'This field must contain a valid NCName.')])),
                ('description', models.TextField(blank=True, null=True)),
                ('definition', models.CharField(blank=True, max_length=512, null=True)),
                ('unit_of_measure', models.CharField(max_length=64)),
                ('wavelength', models.FloatField(blank=True, null=True)),
                ('significant_figures', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('coverage_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='field_types', to='coverages.CoverageType')),
            ],
            options={
                'ordering': ('index',),
            },
        ),
        migrations.CreateModel(
            name='Frame',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(db_index=True, max_length=256, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Grid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, null=True, unique=True, validators=[django.core.validators.RegexValidator(re.compile(b'^[a-zA-z_][a-zA-Z0-9_]*$'), message=b'This field must contain a valid Name.')])),
                ('coordinate_reference_system', models.TextField()),
                ('axis_1_name', models.CharField(max_length=256)),
                ('axis_2_name', models.CharField(blank=True, max_length=256, null=True)),
                ('axis_3_name', models.CharField(blank=True, max_length=256, null=True)),
                ('axis_4_name', models.CharField(blank=True, max_length=256, null=True)),
                ('axis_1_type', models.SmallIntegerField(choices=[(0, b'spatial'), (1, b'elevation'), (2, b'temporal'), (3, b'other')])),
                ('axis_2_type', models.SmallIntegerField(blank=True, choices=[(0, b'spatial'), (1, b'elevation'), (2, b'temporal'), (3, b'other')], null=True)),
                ('axis_3_type', models.SmallIntegerField(blank=True, choices=[(0, b'spatial'), (1, b'elevation'), (2, b'temporal'), (3, b'other')], null=True)),
                ('axis_4_type', models.SmallIntegerField(blank=True, choices=[(0, b'spatial'), (1, b'elevation'), (2, b'temporal'), (3, b'other')], null=True)),
                ('axis_1_offset', models.CharField(max_length=256)),
                ('axis_2_offset', models.CharField(blank=True, max_length=256, null=True)),
                ('axis_3_offset', models.CharField(blank=True, max_length=256, null=True)),
                ('axis_4_offset', models.CharField(blank=True, max_length=256, null=True)),
                ('resolution', models.PositiveIntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Mask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=1024)),
                ('format', models.CharField(blank=True, max_length=64, null=True)),
                ('geometry', django.contrib.gis.db.models.fields.GeometryField(blank=True, null=True, srid=4326)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MaskType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=512, validators=[django.core.validators.RegexValidator(re.compile(b'^[a-zA-z_][a-zA-Z0-9_]*$'), message=b'This field must contain a valid Name.')])),
            ],
        ),
        migrations.CreateModel(
            name='MetaDataItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=1024)),
                ('format', models.CharField(blank=True, max_length=64, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='NilValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=512)),
                ('reason', models.CharField(choices=[(b'http://www.opengis.net/def/nil/OGC/0/inapplicable', b'Inapplicable (There is no value)'), (b'http://www.opengis.net/def/nil/OGC/0/missing', b'Missing'), (b'http://www.opengis.net/def/nil/OGC/0/template', b'Template (The value will be available later)'), (b'http://www.opengis.net/def/nil/OGC/0/unknown', b'Unknown'), (b'http://www.opengis.net/def/nil/OGC/0/withheld', b'Withheld (The value is not divulged)'), (b'http://www.opengis.net/def/nil/OGC/0/AboveDetectionRange', b'Above detection range'), (b'http://www.opengis.net/def/nil/OGC/0/BelowDetectionRange', b'Below detection range')], max_length=512)),
                ('field_types', models.ManyToManyField(blank=True, related_name='nil_values', to='coverages.FieldType')),
            ],
        ),
        migrations.CreateModel(
            name='OrbitNumber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(db_index=True, max_length=256, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProcessingCenter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(db_index=True, max_length=256, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProcessingMode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(db_index=True, max_length=256, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProcessorName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(db_index=True, max_length=256, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProductMetadata',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parent_identifier', models.CharField(blank=True, db_index=True, max_length=256, null=True)),
                ('production_status', models.PositiveSmallIntegerField(blank=True, choices=[(0, b'ARCHIVED'), (1, b'ACQUIRED'), (2, b'CANCELLED')], db_index=True, null=True)),
                ('acquisition_type', models.PositiveSmallIntegerField(blank=True, choices=[(0, b'NOMINAL'), (1, b'CALIBRATION'), (2, b'OTHER')], db_index=True, null=True)),
                ('orbit_direction', models.PositiveSmallIntegerField(blank=True, choices=[(0, b'ASCENDING'), (1, b'DESCENDING')], db_index=True, null=True)),
                ('product_quality_status', models.PositiveSmallIntegerField(blank=True, choices=[(0, b'NOMINAL'), (1, b'DEGRAGED')], db_index=True, null=True)),
                ('creation_date', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('modification_date', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('processing_date', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('availability_time', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('start_time_from_ascending_node', models.IntegerField(blank=True, db_index=True, null=True)),
                ('completion_time_from_ascending_node', models.IntegerField(blank=True, db_index=True, null=True)),
                ('illumination_azimuth_angle', models.FloatField(blank=True, db_index=True, null=True)),
                ('illumination_zenith_angle', models.FloatField(blank=True, db_index=True, null=True)),
                ('illumination_elevation_angle', models.FloatField(blank=True, db_index=True, null=True)),
                ('polarisation_mode', models.PositiveSmallIntegerField(blank=True, choices=[(0, b'single'), (1, b'dual'), (2, b'twin'), (3, b'quad'), (4, b'UNDEFINED')], db_index=True, null=True)),
                ('polarization_channels', models.PositiveSmallIntegerField(blank=True, choices=[(0, b'HV'), (1, b'HV, VH'), (2, b'VH'), (3, b'VV'), (4, b'HH, VV'), (5, b'HH, VH'), (6, b'HH, HV'), (7, b'VH, VV'), (8, b'VH, HV'), (9, b'VV, HV'), (10, b'VV, VH'), (11, b'HH'), (12, b'HH, HV, VH, VV'), (13, b'UNDEFINED')], db_index=True, null=True)),
                ('antenna_look_direction', models.PositiveSmallIntegerField(blank=True, choices=[(0, b'LEFT'), (1, b'RIGHT')], db_index=True, null=True)),
                ('minimum_incidence_angle', models.FloatField(blank=True, db_index=True, null=True)),
                ('maximum_incidence_angle', models.FloatField(blank=True, db_index=True, null=True)),
                ('doppler_frequency', models.FloatField(blank=True, db_index=True, null=True)),
                ('incidence_angle_variation', models.FloatField(blank=True, db_index=True, null=True)),
                ('cloud_cover', models.FloatField(blank=True, db_index=True, null=True)),
                ('snow_cover', models.FloatField(blank=True, db_index=True, null=True)),
                ('lowest_location', models.FloatField(blank=True, db_index=True, null=True)),
                ('highest_location', models.FloatField(blank=True, db_index=True, null=True)),
                ('acquisition_station', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='metadatas', to='coverages.AcquisitionStation')),
                ('acquisition_sub_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='metadatas', to='coverages.AcquisitionSubType')),
                ('archiving_center', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='metadatas', to='coverages.ArchivingCenter')),
                ('frame', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='metadatas', to='coverages.Frame')),
                ('orbit_number', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='metadatas', to='coverages.OrbitNumber')),
                ('processing_center', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='metadatas', to='coverages.ProcessingCenter')),
                ('processing_mode', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='metadatas', to='coverages.ProcessingMode')),
                ('processor_name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='metadatas', to='coverages.ProcessorName')),
            ],
        ),
        migrations.CreateModel(
            name='ProductQualityDegredationTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(db_index=True, max_length=256, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProductType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=512, unique=True, validators=[django.core.validators.RegexValidator(re.compile(b'^[a-zA-z_][a-zA-Z0-9_]*$'), message=b'This field must contain a valid Name.')])),
                ('allowed_coverage_types', models.ManyToManyField(blank=True, to='coverages.CoverageType')),
            ],
        ),
        migrations.CreateModel(
            name='ProductVersion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(db_index=True, max_length=256, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SensorMode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(db_index=True, max_length=256, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SwathIdentifier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(db_index=True, max_length=256, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(db_index=True, max_length=256, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('eoobject_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='coverages.EOObject')),
            ],
            bases=('coverages.eoobject',),
        ),
        migrations.CreateModel(
            name='Coverage',
            fields=[
                ('eoobject_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='coverages.EOObject')),
                ('axis_1_origin', models.CharField(blank=True, max_length=256, null=True)),
                ('axis_2_origin', models.CharField(blank=True, max_length=256, null=True)),
                ('axis_3_origin', models.CharField(blank=True, max_length=256, null=True)),
                ('axis_4_origin', models.CharField(blank=True, max_length=256, null=True)),
                ('axis_1_size', models.PositiveIntegerField()),
                ('axis_2_size', models.PositiveIntegerField(blank=True, null=True)),
                ('axis_3_size', models.PositiveIntegerField(blank=True, null=True)),
                ('axis_4_size', models.PositiveIntegerField(blank=True, null=True)),
                ('collections', models.ManyToManyField(blank=True, related_name='coverages', to='coverages.Collection')),
                ('coverage_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='coverages.CoverageType')),
                ('grid', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='coverages.Grid')),
            ],
            options={
                'abstract': False,
            },
            bases=('coverages.eoobject', models.Model),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('eoobject_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='coverages.EOObject')),
                ('collections', models.ManyToManyField(blank=True, related_name='products', to='coverages.Collection')),
                ('package', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='backends.Storage')),
                ('product_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='coverages.ProductType')),
            ],
            bases=('coverages.eoobject',),
        ),
        migrations.CreateModel(
            name='ReservedID',
            fields=[
                ('eoobject_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='coverages.EOObject')),
                ('until', models.DateTimeField(blank=True, null=True)),
                ('request_id', models.CharField(blank=True, max_length=256, null=True)),
            ],
            bases=('coverages.eoobject',),
        ),
        migrations.AddField(
            model_name='productmetadata',
            name='product_quality_degradation_tag',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='metadatas', to='coverages.ProductQualityDegredationTag'),
        ),
        migrations.AddField(
            model_name='productmetadata',
            name='product_version',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='metadatas', to='coverages.ProductVersion'),
        ),
        migrations.AddField(
            model_name='productmetadata',
            name='sensor_mode',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='metadatas', to='coverages.SensorMode'),
        ),
        migrations.AddField(
            model_name='productmetadata',
            name='swath_identifier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='metadatas', to='coverages.SwathIdentifier'),
        ),
        migrations.AddField(
            model_name='productmetadata',
            name='track',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='metadatas', to='coverages.Track'),
        ),
        migrations.AddField(
            model_name='metadataitem',
            name='eo_object',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='metadata_items', to='coverages.EOObject'),
        ),
        migrations.AddField(
            model_name='metadataitem',
            name='storage',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='backends.Storage'),
        ),
        migrations.AddField(
            model_name='masktype',
            name='product_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mask_types', to='coverages.ProductType'),
        ),
        migrations.AddField(
            model_name='mask',
            name='mask_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coverages.MaskType'),
        ),
        migrations.AddField(
            model_name='mask',
            name='storage',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='backends.Storage'),
        ),
        migrations.AddField(
            model_name='collectiontype',
            name='allowed_coverage_types',
            field=models.ManyToManyField(blank=True, to='coverages.CoverageType'),
        ),
        migrations.AddField(
            model_name='collectiontype',
            name='allowed_product_types',
            field=models.ManyToManyField(blank=True, to='coverages.ProductType'),
        ),
        migrations.AddField(
            model_name='browsetype',
            name='product_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coverages.ProductType'),
        ),
        migrations.AddField(
            model_name='browse',
            name='browse_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='coverages.BrowseType'),
        ),
        migrations.AddField(
            model_name='browse',
            name='storage',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='backends.Storage'),
        ),
        migrations.AddField(
            model_name='arraydataitem',
            name='coverage',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='arraydata_items', to='coverages.EOObject'),
        ),
        migrations.AddField(
            model_name='arraydataitem',
            name='storage',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='backends.Storage'),
        ),
        migrations.AddField(
            model_name='allowedvaluerange',
            name='field_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='allowed_value_ranges', to='coverages.FieldType'),
        ),
        migrations.AddField(
            model_name='productmetadata',
            name='product',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='product_metadata', to='coverages.Product'),
        ),
        migrations.AlterUniqueTogether(
            name='masktype',
            unique_together=set([('name', 'product_type')]),
        ),
        migrations.AddField(
            model_name='mask',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='masks', to='coverages.Product'),
        ),
        migrations.AlterUniqueTogether(
            name='fieldtype',
            unique_together=set([('identifier', 'coverage_type'), ('index', 'coverage_type')]),
        ),
        migrations.AddField(
            model_name='coveragemetadata',
            name='coverage',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='coverage_metadata', to='coverages.Coverage'),
        ),
        migrations.AddField(
            model_name='coverage',
            name='parent_product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='coverages', to='coverages.Product'),
        ),
        migrations.AddField(
            model_name='collectionmetadata',
            name='collection',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='collection_metadata', to='coverages.Collection'),
        ),
        migrations.AddField(
            model_name='collection',
            name='collection_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='coverages.CollectionType'),
        ),
        migrations.AddField(
            model_name='collection',
            name='grid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='coverages.Grid'),
        ),
        migrations.AlterUniqueTogether(
            name='browsetype',
            unique_together=set([('name', 'product_type')]),
        ),
        migrations.AddField(
            model_name='browse',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='browses', to='coverages.Product'),
        ),
        migrations.AlterUniqueTogether(
            name='arraydataitem',
            unique_together=set([('coverage', 'field_index')]),
        ),
        migrations.AlterUniqueTogether(
            name='browse',
            unique_together=set([('product', 'browse_type', 'style')]),
        ),
    ]
