
### Falcon Resource Factory

[![version](https://img.shields.io/pypi/v/falcon-resource-factory.svg)](https://pypi.python.org/pypi/falcon-resource-factory/)
[![Build Status](https://travis-ci.org/loanzen/falcon-resource-factory.svg?branch=master)](https://travis-ci.org/loanzen/falcon-resource-factory)
[![License](http://img.shields.io/:license-mit-blue.svg)](https://pypi.python.org/pypi/falcon-resource-factory/)
[![Wheel](https://img.shields.io/pypi/wheel/factory-resource-factory.svg)](https://pypi.python.org/pypi/falcon-resource-factory/)


A simple falcon library that allows defining a single resource class to 
handle requests for a single item as well as multiple items. While though its not 
purely `RESTful`, sometimes you require your resource to support custom endpoints. 
The library allows you to define such custom endpoints as well as part of the same 
single resource class.


#### Installation

Install the library using pip, or easy_install.

    $ pip install -U falcon-resource-factory
    

#### Usage

This library exposes a single class `falcon_resource_factory.ResourceFactory` 
which is used to add your single resource class to falcon as shown below.
 
    import falcon
    from falcon_resource_factory import ResourceFactory
    
    api = falcon.API()
    
    class Resource(object):
        def on_get(req, res, **kwargs):
            # Return single object
            pass
                     
        def on_get_list(req, res, **kwargs):
            # Returns list of objects
            pass

    
    resource_factory = ResourceFactory()
    resource_factory.add_routes(app, '/res', Resource())
    

The `ResourceFactory` instance will create two separate resources internally
 called `ResourceDetail` and `ResourceList` for handling single item and 
 list of items respectively and register them with falcon at appropriate routes.
  The generated resources have appropriate handlers for all http methods supported
  by your resource which in turn just wrappers around your resource handlers. 
  
  For eg for the resource defined above, the generated resources
  will look like as follows
  
        class ResourceDetail(object):
            
            def on_get(req, res, **kwargs):
                resource.on_get(req, res, **kwargs):
                
        class ResourceList(object):
            def on_get(req, res, **kwargs):
                resource.on_get_list(req, res, **kwargs):
 
 
##### Custom Detail Identifier


`ResourceFactory` creates the route for detail resource by appending
a resource identifier to the passed route. By default detail identifier is
 `id` but you can change it by passing it to ResourceFactory during initialization
 
    resource_factory = ResourceFactory(detail_identifier='uuid')


##### Custom Method Map

`ResourceFactory` by default maps HTTP methods to handlers in the resource by using 
`<method> : on_<method>` for detail resources and `<method>: on_<method>_list` 
for list resources. However both of them are configiurable during initialization
of `ResourceFactory`.  You can pass a mapping of HTTP methods to methods of your
resources for both list and detail resources.

    resource_factory = ResourceFactory(list_method_map={
        'GET': 'on_get_collection',
        'POST': 'on_post_collection'
        .....
    }, detail_method_map={
        'GET': 'get_obj',
        'POST': 'post_obj'
        ....
    })
    
    
    class Resource(object):
    
        def on_get_collection(req, res, **kwargs)
            pass

        def on_post_collection(req, res, **kwargs)
            pass

        def get_obj(req, res, **kwargs)
            pass

        def post_obj(req, res, **kwargs)
            pass


##### CustomViews

Sometimes, you want to support api's that are not CRUD. In such situations, 
purely RESTful approach suggests that you create more resources instead of defining
custom verbs. However, sometime its easier to define custom endpoints/actions instead
of mapping them to resources which might not be that straightforward. `ResourceFactory` 
support defining custom views by automatically  creating separate resources for 
each custom view and registering with falcon. You need to pass a list of view specs 
to `ResourceFactory` during initialization and it takes care of rest
 
    resource_factory = ResourceFactory(custom_views=[
        {
            "route": "/action1/",
            "view": "action1",
            "methods": ['GET']
        },
        {
            "route": "/action2/",
            "view": "action2",
            "methods": ['POST']
        }
    ])


    class Resource(object):
    
        def on_get(req, res, **kwargs):
            pass
    
        def action1(req, res, **kwargs):
            pass

        def action2(req, res, **kwargs):
            pass
            
 
 
 #### Contributing 
 `falcon-resource-factory` is distributed under MIT License. 
 
 
 Fork the repository to your own account.
 
 Clone the repository to a suitable location on your local machine.
 
 
     $git clone https://github.com/loanzen/falcon-resource-factory.git
 
 To update the project from within the project's folder you can run the following command:
 
     $git pull --rebase
 
 ##### Building 
 
 Install the project's dependencies.
     
     $pip install -r requirements.txt
     $pip install -r requirements-dev.txt
 
 
 ##### Feature Requests
 
 I'm always looking for suggestions to improve this project. If you have a
 suggestion for improving an existing feature, or would like to suggest a
 completely new feature, please file an issue with my [Github repository](https://github.com/loanzen/falcon-resource-factory/issues)
 
 ##### Bug Reports
 
 You may file bug reports on [Github repository](https://github.com/loanzen/falcon-resource-factory/issues)
 
 ##### Pull Requests

 
 Along with my desire to hear your feedback and suggestions,
 I'm also interested in accepting direct assistance in the form of new code or documentation.
 Please feel free to file pull requests against my [Github repository](https://github.com/loanzen/falcon-resource-factory/issues)
 
 ##### Tests

 All pull request should pass the test suite which can launched simply with
 
    python setup.py test
    
  
  
  [1]: 
 

 
 


