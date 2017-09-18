#-------------------------------------------------------------------------------
#
# Project: EOxServer <http://eoxserver.org>
# Authors: Fabian Schindler <fabian.schindler@eox.at>
#
#-------------------------------------------------------------------------------
# Copyright (C) 2015 EOX IT Services GmbH
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


from itertools import chain
from datetime import datetime

from lxml.etree import CDATA
from lxml.builder import ElementMaker
from django.template.loader import render_to_string
from django.conf import settings

from eoxserver.core.util.xmltools import etree, NameSpace, NameSpaceMap, typemap
from eoxserver.core.util.timetools import isoformat
from eoxserver.resources.coverages import models
from eoxserver.services.opensearch.formats.base import (
    BaseFeedResultFormat, ns_dc, ns_georss, ns_media, ns_owc
)
from eoxserver.services.opensearch.config import (
    DEFAULT_EOXS_OPENSEARCH_SUMMARY_TEMPLATE
)


# namespace declarations
ns_atom = NameSpace("http://www.w3.org/2005/Atom", None)
ns_opensearch = NameSpace("http://a9.com/-/spec/opensearch/1.1/", "opensearch")
ns_gml = NameSpace("http://www.opengis.net/gml", "gml")

# namespace map
nsmap = NameSpaceMap(ns_atom, ns_opensearch, ns_dc, ns_georss, ns_media, ns_owc)

# Element factories
ATOM = ElementMaker(namespace=ns_atom.uri, nsmap=nsmap, typemap=typemap)
OS = ElementMaker(namespace=ns_opensearch.uri, nsmap=nsmap)
GML = ElementMaker(namespace=ns_gml.uri, nsmap=nsmap)


class AtomResultFormat(BaseFeedResultFormat):
    """ Atom result format.
    """

    mimetype = "application/atom+xml"
    name = "atom"

    def encode(self, request, collection_id, queryset, search_context):

        namespaces = dict(nsmap)
        namespaces.update(search_context.namespaces)
        ATOM = ElementMaker(namespace=ns_atom.uri, nsmap=namespaces)

        tree = ATOM("feed",
            ATOM("id", request.build_absolute_uri()),
            ATOM("title", "%s Search" % collection_id),
            ATOM("link", rel="self", href=request.build_absolute_uri()),
            ATOM("description"),
            OS("totalResults", str(search_context.total_count)),
            OS("startIndex", str(search_context.start_index or 0)),
            OS("itemsPerPage", str(search_context.count)),
            OS("Query", role="request", **dict(
                ("{%s}%s" % (namespaces[prefix], name), value)
                for prefix, params in search_context.parameters.items()
                for name, value in params.items()
            )),
            *chain(
                self.encode_feed_links(request, search_context), [
                    self.encode_entry(request, item) for item in queryset
                ]
            )
        )
        return etree.tostring(tree, pretty_print=True)

    def encode_entry(self, request, item):
        entry = ATOM("entry",
            ATOM("title", item.identifier),
            ATOM("id", item.identifier),
            self.encode_summary(request, item),
        )

        entry.extend(self.encode_item_links(request, item))
        entry.extend(self.encode_spatio_temporal(item))

        return entry

    def encode_summary(self, request, item):
        template_name = getattr(
            settings, 'EOXS_OPENSEARCH_SUMMARY_TEMPLATE',
            DEFAULT_EOXS_OPENSEARCH_SUMMARY_TEMPLATE
        )

        metadata = []
        coverages = []

        if isinstance(item, models.Coverage):
            coverages = [item]
        elif isinstance(item, models.Product):
            coverages = item.coverages.all()
            metadata = [
                (
                    name.replace('_', ' ').title(),
                    isoformat(value) if isinstance(value, datetime) else str(value)
                )
                for name, value in models.product_get_metadata(item)
            ]

        return ATOM("summary",
            CDATA(render_to_string(
                template_name, {
                    'item': item, 'metadata': metadata,
                    'atom': self._create_self_link(request, item),
                    'map_small': self._create_map_link(request, item, 100),
                    'map_large': self._create_map_link(request, item, 500),
                    'coverages': [{
                        'description': self._create_coverage_description_link(
                            request, coverage
                        ),
                        'coverage': self._create_coverage_link(
                            request, coverage
                        )}
                        for coverage in coverages
                    ]
                },
                request=request
            )),
            type="html"
        )
