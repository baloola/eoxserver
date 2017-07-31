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

from django.core.management.base import CommandError, BaseCommand
from django.db import transaction

from eoxserver.resources.coverages import models
from eoxserver.resources.coverages.management.commands import (
    CommandOutputMixIn, SubParserMixIn
)


class Command(CommandOutputMixIn, SubParserMixIn, BaseCommand):
    """ Command to manage coverage types. This command uses sub-commands for the
        specific tasks: create, delete
    """
    def add_arguments(self, parser):
        create_parser = self.add_subparser(parser, 'create',
            help='Create a new coverage type.'
        )
        delete_parser = self.add_subparser(parser, 'delete',
            help='Delete a coverage type.'
        )
        list_parser = self.add_subparser(parser, 'list')

        for parser in [create_parser, delete_parser]:
            parser.add_argument(
                'name', nargs=1, help='The coverage type name. Mandatory.'
            )

        create_parser.add_argument(
            '--field-type', action='append', nargs=5,
            metavar=(
                'identifier', 'description', 'definition', 'unit-of-measure',
                'wavelength'
            ),
            dest='field_types', default=[],
            help=(
                'Add a field type to the coverage type.'
            )
        )
        delete_parser.add_argument(
            '--force', '-f', action='store_true', default=False,
            help='Also remove all collections associated with that type.'
        )

        list_parser.add_argument(
            '--no-detail', action="store_false", default=True, dest='detail',
            help="Disable the printing of details of the product type."
        )

    @transaction.atomic
    def handle(self, subcommand, *args, **kwargs):
        """ Dispatch sub-commands: create, delete, insert and exclude.
        """
        if subcommand == "create":
            self.handle_create(kwargs['name'][0], *args, **kwargs)
        elif subcommand == "delete":
            self.handle_delete(kwargs['name'][0], *args, **kwargs)
        elif subcommand == "list":
            self.handle_list(*args, **kwargs)

    def handle_create(self, name, field_types, **kwargs):
        """ Handle the creation of a new coverage type.
        """

        coverage_type = models.CoverageType.objects.create(name=name)
        for i, field_type_definition in enumerate(field_types):
            models.FieldType.objects.create(
                coverage_type=coverage_type, index=i,
                identifier=field_type_definition[0],
                description=field_type_definition[1],
                definition=field_type_definition[2],
                unit_of_measure=field_type_definition[3],
                wavelength=field_type_definition[4]
            )

        print('Successfully created coverage type %r' % name)

    def handle_delete(self, name, force, **kwargs):
        """ Handle the deletion of a collection type
        """
        try:
            collection_type = models.CoverageType.objects.get(name=name)

            if force:
                coverages = models.Coverage.objects.filter(
                    coverage_type=coverage_type
                )
                # TODO de-register coverages

            collection_type.delete()
        except models.CoverageType.DoesNotExist:
            raise CommandError('No such coverage type: %r' % name)

        print('Successfully deleted coverage type %r' % name)

    def handle_list(self, detail, *args, **kwargs):
        """ Handle the listing of product types
        """
        for coverage_type in models.CoverageType.objects.all():
            print(coverage_type.name)
            if detail:
                for coverage_type in coverage_type.field_types.all():
                    print("\t%s" % coverage_type.identifier)
