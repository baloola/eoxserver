#-------------------------------------------------------------------------------
# $Id$
#
# Project: EOxServer <http://eoxserver.org>
# Authors: Fabian Schindler <fabian.schindler@eox.at>
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


import itertools
from functools import partial

from eoxserver.core import env, Component, implements, ExtensionPoint

from eoxserver.services.ows.interfaces import *
from eoxserver.services.ows.decoders import get_decoder
from eoxserver.services.exceptions import (
    ServiceNotSupportedException, VersionNotSupportedException,
    VersionNegotiationException, OperationNotSupportedException
)
from eoxserver.services.ows.common.v20.exceptionhandler import (
    OWS20ExceptionHandler
)


class ServiceComponent(Component):
    service_handlers = ExtensionPoint(ServiceHandlerInterface)
    exception_handlers = ExtensionPoint(ExceptionHandlerInterface)

    get_service_handlers = ExtensionPoint(GetServiceHandlerInterface)
    post_service_handlers = ExtensionPoint(PostServiceHandlerInterface)

    version_negotiation_handlers = ExtensionPoint(VersionNegotiationInterface)


    def __init__(self, *args, **kwargs):
        super(ServiceComponent, self).__init__(*args, **kwargs)


    def query_service_handler(self, request):
        """ Tries to find the correct service handler
        """

        decoder = get_decoder(request)
        if request.method == "GET":
            handlers = self.get_service_handlers 
        elif request.method == "POST":
            handlers = self.post_service_handlers 
        else:
            handlers = self.service_handlers

        version = decoder.version
        if version is None:
            accepted_versions = decoder.acceptversions
            handlers = filter_handlers(
                handlers, decoder.service, accepted_versions, decoder.request
            )
            return self.version_negotiation(handlers, accepted_versions)

        # check that the service is supported
        handlers = filter(
            partial(handler_supports_service, service=decoder.service), handlers
        )
        if not handlers:
            raise ServiceNotSupportedException(decoder.service)

        # check that the required version is enabled
        handlers_ = filter(
            lambda h: decoder.version in h.versions, handlers
        )
        if not handlers_:
            # old style version negotiation shall always return capabilities
            if decoder.request == "GETCAPABILITIES":
                handlers = [sorted(
                    filter(
                        lambda h: decoder.request == h.request.upper(), handlers
                    ), key=lambda h: max(h.versions), reverse=True
                )[0]]
            else:
                raise VersionNotSupportedException(decoder.service, decoder.version)
        else:
            handlers = handlers_

        # check that the required operation is supported and sort by the highest
        # version supported in descending manner
        handlers = sorted(
            filter(
                lambda h: decoder.request == h.request.upper(), handlers
            ), key=lambda h: max(h.versions), reverse=True
        )

        if not handlers:
            operation = decoder.request
            raise OperationNotSupportedException(
                "Operation '%s' is not supported." % operation, operation
            )

        # return the handler with the highest version
        return handlers[0]


    def query_service_handlers(self, service=None, versions=None, request=None, method=None):
        method = method.upper() if method is not None else None

        if method == "GET":
            handlers = self.get_service_handlers
        elif method == "POST":
            handlers = self.post_service_handlers
        elif method is None:
            handlers = self.service_handlers
        else:
            return []

        handlers = filter_handlers(handlers, service, versions, request)
        return sort_handlers(handlers)


    def query_exception_handler(self, request):
        decoder = get_decoder(request)
        handlers = self.exception_handlers

        handlers = sorted(
            filter(
                partial(handler_supports_service, service=decoder.service), 
                self.exception_handlers
            ),
            key=lambda h: max(h.versions), reverse=True
        )

        # try to get the correctly versioned exception handler
        if decoder.version:
            for handler in handlers:
                if decoder.version in handler.versions:
                    return handler
        else:
            # return the exception handler with the highest version,
            # if one is available
            try:
                return handlers[0]
            except IndexError:
                pass

        # last resort fallback is a plain OWS exception handler
        return OWS20ExceptionHandler()


    def version_negotiation(self, handlers, accepted_versions=None):
        version_to_handler = {}
        for handler in handlers:
            for version in handler.versions:
                version_to_handler.setdefault(version, handler)

        available_versions = sorted(version_to_handler.keys(), reverse=True)
        if not available_versions:
            raise VersionNegotiationException()

        if not accepted_versions:
            return version_to_handler[available_versions[0]]

        combinations = itertools.product(accepted_versions, available_versions)
        for accepted_version, available_version in combinations:
            if accepted_version == available_version:
                return version_to_handler[available_version]

        raise VersionNegotiationException()


def filter_handlers(handlers, service=None, versions=None, request=None):
    """ Utility function to filter the given OWS service handlers by their
        attributes 'service', 'versions' and 'request'.
    """

    service = service.upper() if service is not None else None
    request = request.upper() if request is not None else None

    if service:
        handlers = filter(
            partial(handler_supports_service, service=service), handlers
        )

    if request:
        handlers = filter(lambda h: h.request.upper() == request, handlers)

    if versions:
        handlers = [
            handler for handler in handlers
            if any(version in handler.versions for version in versions)
        ]

    return handlers


def sort_handlers(handlers, ascending=True):
    return sorted(
        handlers, key=lambda h: getattr(h, "index", 100000), 
        reverse=not ascending
    )


def handler_supports_service(handler, service=None):
    """ Convenience method to check whether or not a handler supports a service.
    """
    if isinstance(handler.service, basestring):
        return handler.service.upper() == service
    else:
        return service in handler.service
