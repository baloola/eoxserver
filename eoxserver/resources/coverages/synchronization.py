#-------------------------------------------------------------------------------
#
# Project: EOxServer <http://eoxserver.org>
# Authors: Fabian Schindler <fabian.schindler@eox.at>
#
#-------------------------------------------------------------------------------
# Copyright (C) 2014 EOX IT Services GmbH
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

"""
This module provides functionality to synchronize the database models in one
collection with the contents on a storage.
"""

import logging
import re
import os.path

from eoxserver.core import env
from eoxserver.backends.access import retrieve
from eoxserver.backends import models as backends
from eoxserver.backends.component import BackendComponent
from eoxserver.resources.coverages import models
from eoxserver.resources.coverages.registration.component import (
    RegistratorComponent
)


logger = logging.getLogger(__name__)

# TODO: create regexes

TEMPLATE_RE = re.compile(
    r"template\[(?P<value>[a-zA-Z0-9_\[\]]+)\]", re.IGNORECASE
)
SOURCE_RE = re.compile(
    r"source\[(?P<value>[a-zA-Z0-9_\[\]]+)\]", re.IGNORECASE
)
#SOURCE_RE = re.compile(r"source\[*\]", re.IGNORECASE)


class SynchronizationError(Exception):
    pass


def synchronize(collection, recursive=False):
    """ Synchronizes a :class:`eoxserver.resources.coverages.models.Collection`
        and all its data sources with their respective storages.
    """

    # allow both model and identifier
    if isinstance(collection, basestring):
        collection = models.Collection.objects.get(identifier=collection)

    collection = collection.cast()

    if recursive:
        synchronize(
            models.Collection.objects.filter(collections__in=[collection.pk]),
            recursive
        )

    logger.info("Synchronizing collection %s" % collection)

    all_paths = []
    for data_source in collection.data_sources.all():
        all_paths.extend(
            _expand_data_source(data_source)
        )

    # loop over all paths and check if there is already a dataset registered
    # for it.
    for paths in all_paths:
        exists = True
        for filename, data_item, semantic in paths:
            exists = backends.DataItem.objects.filter(
                package=data_item.package, storage=data_item.storage,
                location=filename
            ).exists()
            if not exists:
                break

        if not exists:
            logger.info("Creating new dataset.")
            for registrator in RegistratorComponent(env).registrators:
                # TODO: select registrator
                pass

            registrator.register(
                items, overrides, cache
            )

    # loop over all coverages in this collection. if any is not represented by
    # its referenced file, delete it.
    contained = models.Coverage.objects.filter(collections__in=[collection.pk])
    for coverage in contained:
        data_items = tuple(coverage.data_items)
        all_exists = False
        for existing_data_item in data_items:
            files_exist = False
            for paths in all_paths:
                for filename, data_item, semantic in paths:
                    if existing_data_item.location == filename and \
                            existing_data_item.semantic == semantic:
                        files_exist = True
                        break
            if files_exist:
                break

def _expand_data_source(data_source):
    """ Helper function to loop over all files referenced by a data source.
    """

    data_items = tuple(data_source.data_items.all())

    # detect the template data items and the primary data item of a data source
    template_data_items = [
        data_item for data_item in data_items
        if TEMPLATE_RE.match(data_item.semantic)
    ]
    primary_data_items = [
        data_item for data_item in data_items
        if SOURCE_RE.match(data_item.semantic)
    ]

    if len(primary_data_items) == 0:
        raise SynchronizationError(
            "No primary data item for data source specified."
        )
    elif len(primary_data_items) > 1:
        raise SynchronizationError(
            "Too many primary data items for data source specified."
        )
    else:
        primary_data_item = primary_data_items[0]

    primary_sem = SOURCE_RE.match(primary_data_item.semantic).group("value")

    # TODO: expand data item to filenames

    files = _expand_data_item(primary_data_item)
    if not files:
        logger.info(
            "Data source %s did not match any files." % primary_data_item
        )
    else:
        logger.info(
            "Data source %s matched %d files." % (primary_data_item, len(files))
        )

    # TODO: probably replace this with a generator based solution

    all_paths = []
    for filename in files:
        # each template must match exactly one file
        dirname, basename = os.path.split(filename)
        _, ext = os.path.splitext(basename)
        template_values = {
            "basename": basename,
            "dirname": dirname,
            "extension": ext,
        }

        paths = [(filename, primary_data_item, primary_sem)]
        for template_data_item in template_data_items:
            template_sem = TEMPLATE_RE.match(
                template_data_item.semantic
            ).group("value")

            template_files = _expand_template_data_item(
                template_data_item, template_values
            )

            # TODO: check count

            paths.append((template_files, template_data_item, template_sem))

        all_paths.append(paths)

    return all_paths


def _expand_data_item(data_item, cache=None):
    """ Helper function to expand a source data item to a list of file
        identifiers.
    """

    backends = BackendComponent(env)

    storage = data_item.storage
    package = data_item.package

    if storage:
        # get list of files of that storage
        component = backends.get_storage_component(storage.storage_type)
        if not component:
            raise ValueError(
                "No storage component for type '%s' found."
                % storage.storage_type
            )

        return component.list_files(storage.url, data_item.location)

    elif package:
        # get list of files of that package
        local_filename = retrieve(package, cache)
        component = backends.get_package_component(package.format)
        if not component:
            raise ValueError(
                "No package component for type '%s' found."
                % package.format
            )

        return component.list_files(local_filename, data_item.location)

    else:
        # This is a local filename, expand it directly
        component = backends.get_storage_component("local")
        if not component:
            raise ValueError("No active local storage component found.")

        return component.list_files("", data_item.location)


def _expand_template_data_item(data_item, template_values, cache=None):
    """ Helper function to expand a source data item to a list of file
        identifiers, but first expanding the template location with the string
        format syntax.
    """

    location = data_item.location

    try:
        data_item.location = location.format(template_values)
    except:
        try:
            data_item.location = location % template_values
        except:
            raise ValueError(
                "Invalid template '%s' in template data item %s."
                % (location, data_item)
            )

    return _expand_data_item(data_item, cache)
