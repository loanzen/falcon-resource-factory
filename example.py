# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division

import falcon
from falcon_resource_factory import ResourceFactory


api = falcon.API()


class DummyResource(object):
    CUSTOM_VIEWS = [
        {
            'route': '/custom_view',
            'view': 'custom_view',
            'methods': ['GET']
        }
    ]

    def on_post(self, req, res, *args, **kwargs):
        pass

    def on_get_list(self, req, res, *args, **kwargs):
        pass

    def custom_view(self, req, res, *args, **kwargs):
        pass

resource_factory = ResourceFactory(custom_views=DummyResource.CUSTOM_VIEWS)
resource_factory.add_routes(api, '/dummy/', DummyResource())
