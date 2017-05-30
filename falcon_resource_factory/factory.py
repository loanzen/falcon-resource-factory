# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division

from falcon_resource_factory import utils


__all__ = ['ResourceFactory']


class ResourceFactory(object):
    """
    ``ResourceFactory`` is the main class for this package. It main purpose is
    to allow single resource class for handling requests for both detail and collection
    of items. The way it works is that you call its `add_routes` method with a
    `falcon.API`, route and a resource object and it registers two separate resources
    one for handling requests for detail items and one for handling collection of
    items. The generated resources uses a configurable mapping from
    `http verbs` to `method names` to call appropriate handlers in the original
    resource. By default the mappings are defined in two class variables
    `LIST_METHOD_MAP` and `DETAIL_METHOD_MAP` for collection and detail requests
    respectively. But they can be customized by passing custom method maps for
    both list and detail resources during initialization.

    While not being purely `RESTful` sometimes you require your resource to
    support custom endpoints. `ResourceFactory` allows you to define custom views
    inside the same single resource by passing a list of custom views during
    initialization. It creates separate resource for each custom view and register
    it with `falcon.API` at proper endpoint.

    You speficy a custom view as follows

        ```
        {
            "route": "<custom endpoint/action>",
            "view": "<resource factory method that implements this view>",
            "methods": <List of supported methods>
        }

        ```

    NOTE: When you call the ``add_route`` method to register routes with the falcon
    app, you specify a route param which is used as-is for list routes. For detail
    routes we concatenate the route with `detail_identifier` param which is passed during
    initializtion or `id` by default. For custom views, we concatenate the route
    with the custom view's route param. Also for both custom and detail uri, we
    append a trailing slash if the original route param also had a trailing slash
    to keep common behaviour across the routes.
    """

    # A map from `http verb` to method name for list routes
    LIST_METHOD_MAP = {
        'GET': 'on_get_list',
        'POST': 'on_post_list',
        'PUT': 'on_put_list',
        'PATCH': 'on_patch_list',
        'DELETE': 'on_delete_list'
    }

    # A map from `http verb` to method name for detail routes
    DETAIL_METHOD_MAP = {
        'GET': 'on_get',
        'POST': 'on_post',
        'PUT': 'on_put',
        'PATCH': 'on_patch',
        'DELETE': 'on_delete'
    }

    def __init__(self,
                 list_method_map=None,
                 detail_method_map=None,
                 detail_identifier='id',
                 custom_views=None):
        """
        :param list_method_map: allows customizing mapping from http verb to method name
            for list routes
        :param detail_method_map: allows customizing mapping from http verb to method name
            for detail routes
        :param detail_identifier: name of the detail route identifier (Defaut is 'id') to be
            used for detail routes
        :params custom_views: list of custom views in format mentioned above.

        """
        self.list_method_map = list_method_map or dict(self.LIST_METHOD_MAP)
        self.detail_method_map = detail_method_map or dict(self.DETAIL_METHOD_MAP)
        self.detail_identifier = detail_identifier
        self.custom_views = custom_views or []

    def add_routes(self, app, route, resource):
        """
        Creates list, detail and custom resource wrapper for the specified resource
        and registers them with the falcon `app` at the specified `route`
        :param app: falcon app
        :param route: base route to be used for this resource
        :param resource: a resource object implementing list, detail and custom views
        :return:
        """
        params = self._get_resource_params(resource)
        self._create_detail_resource(app, route, resource, params)
        self._create_list_resource(app, route, resource, params)
        self._create_custom_views(app, route, resource, params)

    def _get_resource_params(self, resource):
        return dict(
            (attr, getattr(resource, attr)) for attr in dir(resource)
            if not callable(getattr(resource, attr)) and not attr.startswith("__")
        )

    def _create_route(self, route, part):
        has_trailing_slash = route[-1] == '/'
        route = '/'.join(map(lambda x: str(x).rstrip('/'), [route, part])).replace('//', '/')
        if has_trailing_slash:
            route += '/'
        return route

    def _create_detail_resource(self, app, route, resource, params):
        route = self._create_route(route,
                                   '{{{0}}}'.format(self.detail_identifier))
        res_cls = '{0}Detail'.format(resource.__class__.__name__)
        wrapper_cls = type(res_cls, (), params)
        app.add_route(route, self._wrap_resource(wrapper_cls, resource,
                                                 self.detail_method_map))

    def _create_list_resource(self, app, route, resource, params):
        res_cls = '{0}List'.format(resource.__class__.__name__)
        wrapper_cls = type(res_cls, (), params)
        app.add_route(route, self._wrap_resource(wrapper_cls, resource,
                                                 self.list_method_map))

    def _create_custom_views(self, app, route, resource, params):
        for view in self.custom_views:
            res_cls = '{0}{1}'.format(resource.__class__.__name__,
                                      utils.underscore_camelcase_converter(
                                        view['view']))

            if not getattr(resource, view['view']):
                raise NameError('Invalid custom view {}'.format(view['view']))

            wrapper_cls = type(res_cls, (), params)

            method_map = dict((method, view['view']) for method in view['methods'])
            route = self._create_route(route, view['route'])
            app.add_route(route, self._wrap_resource(wrapper_cls, resource,
                                                     method_map))

    def _wrap_resource(self, wrapper_cls, resource, method_map):
        for method, view in method_map.items():
            func_name = 'on_{0}'.format(method.lower())
            func = getattr(resource, view, None)
            if func:
                setattr(wrapper_cls, func_name, func)

        return wrapper_cls()
