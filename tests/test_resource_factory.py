# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division

import falcon
import pytest
from falcon import testing
from falcon.cmd.print_routes import print_routes

from falcon_resource_factory import ResourceFactory


def detail_view(resource, req, res, **kwargs):
    res.body = '{} Called'.format(req.method)


def list_view(resource, req, res, **kwargs):
    res.body = '{} list Called'.format(req.method)


def resource_creator(detail_methods, list_methods,
                     detail_method_map=ResourceFactory.DETAIL_METHOD_MAP,
                     list_method_map=ResourceFactory.LIST_METHOD_MAP,
                     custom_views=None, params=None):

    test_resource = type('TestResource', (), params or {})
    for method in detail_methods:
        func_name = detail_method_map[method]
        setattr(test_resource, func_name, detail_view)

    for method in list_methods:
        func_name = list_method_map[method]
        setattr(test_resource, func_name, list_view)

    return test_resource()


@pytest.fixture()
def app():
    return falcon.API()


@pytest.fixture
def client(app):
    return testing.TestClient(app)


@pytest.fixture()
def resource_factory():
    return ResourceFactory()


def _test_detail_routes(app, client, expected_params):
    resource, method_map, params, uri_template = app._router.find('/items/5')

    assert expected_params == params
    assert resource.__class__.__name__ == 'TestResourceDetail'
    assert hasattr(resource, 'on_get')
    assert hasattr(resource, 'on_post')

    response = client.simulate_get('/items/5')
    assert response.content.lower() == b'get called'

    response = client.simulate_post('/items/5')
    assert response.content.lower() == b'post called'


def test_detail_routes(app, resource_factory, client):
    res = resource_creator(['GET', 'POST'], [])
    resource_factory.add_routes(app, '/items/', res)
    expected_params = {'id': '5'}
    _test_detail_routes(app, client, expected_params)


def test_detail_routes_custom_identifier(app, client):
    resource_factory = ResourceFactory(detail_identifier='uuid')
    res = resource_creator(['GET', 'POST'], [])
    resource_factory.add_routes(app, '/items/', res)
    expected_params = {'uuid': '5'}

    _test_detail_routes(app, client, expected_params)


def test_detail_routes_custom_method_map(app, client):
    detail_method_map = {
        'GET': 'obj_get',
        'POST': 'obj_post'
    }

    resource_factory = ResourceFactory(detail_method_map=detail_method_map)
    res = resource_creator(detail_method_map.keys(), [],
                           detail_method_map=detail_method_map)
    resource_factory.add_routes(app, '/items/', res)
    expected_params = {'id': '5'}
    _test_detail_routes(app, client, expected_params)


def _test_list_routes(app, client):
    resource, method_map, params, uri_template = app._router.find('/items')

    assert hasattr(resource, 'on_get')
    assert hasattr(resource, 'on_put')

    assert resource.__class__.__name__ == 'TestResourceList'

    response = client.simulate_get('/items/')
    assert response.content.lower() == b'get list called'

    response = client.simulate_put('/items/')
    assert response.content.lower() == b'put list called'


def test_list_routes(app, resource_factory, client):
    res = resource_creator([], ['GET', 'PUT'])
    resource_factory.add_routes(app, '/items/', res)
    _test_list_routes(app, client)


def test_list_routes_custom_method_map(app, client):
    list_method_map = {
        'GET': 'obj_get_list',
        'PUT': 'obj_put_list'
    }

    resource_factory = ResourceFactory(list_method_map=list_method_map)
    res = resource_creator([], list_method_map.keys(),
                           list_method_map=list_method_map)
    resource_factory.add_routes(app, '/items/', res)
    _test_list_routes(app, client)


def test_generated_resources_has_params(app, resource_factory, client):
    const_parmas = {
        'PARAM_1': '1',
        'PARAM_2': '2',
    }

    hidden_params = {
        '__x': 'hidden',
        'func': lambda: None
    }

    params = dict(const_parmas)
    params.update(dict(hidden_params))

    res = resource_creator(['GET'], ['GET'], params=params)
    resource_factory.add_routes(app, '/items/', res)

    list_resource, _, _, _ = app._router.find('/items')

    list_resource_cls = list_resource.__class__

    for key, val in const_parmas.items():
        assert getattr(list_resource_cls, key) == val

    for key in hidden_params.keys():
        assert not hasattr(list_resource_cls, key)