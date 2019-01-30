===========
gblackboard
===========


.. image:: https://img.shields.io/pypi/v/gblackboard.svg
        :target: https://pypi.python.org/pypi/gblackboard

.. image:: https://img.shields.io/travis/GTedHa/gblackboard.svg
        :target: https://travis-ci.org/GTedHa/gblackboard

.. image:: https://readthedocs.org/projects/gblackboard/badge/?version=latest
        :target: https://gblackboard.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




Blackboard pattern implementation


* Free software: MIT license
* Documentation: https://gblackboard.readthedocs.io.
* Repository: https://github.com/GTedHa/gblackboard


Features
-------

* To be updated
* Refer to 'Usage'


Usage
-------

To use gblackboard in a project:

- basic usage::

    from gblackboard import Blackboard
    from gblackboard import SupportedMemoryType

    blackboard = Blackboard(SupportedMemoryType.DICTIONARY)
    # setup blackboard, it should be called once before using blackboard
    blackboard.setup()
    # set a key-value data; `set` method should be called only once for a key.
    # it's a kind of initialization.
    # supported data-type: int, int[], float, float[], str, str[], dict, dict[]
    blackboard.set('key', 'value')
    # retrieve data with key
    value = blackboard.get('key')
    # update data with new value;
    # `update` method should be called after `set` method called for a key.
    blackboard.update('key', 'new_value')
    # delete data from blackboard with key
    blackboard.drop('key')
    # clear all data in blackboard
    blackboard.clear()

- observer::

    from gblackboard import Blackboard
    from gblackboard import SupportedMemoryType

    def callback(data):
        print(data)

    blackboard = Blackboard(SupportedMemoryType.DICTIONARY)
    blackboard.setup()
    blackboard.set('key', 'value')
    # register callback
    blackboard.register_callback('key', callback)
    # update data, `callback` function will be called during `update`
    # and `new_value` will passed to `callback` function.
    blackboard.update('key', 'new_value')

- complex data::

    from gblackboard import Blackboard
    from gblackboard import SupportedMemoryType

    from marshmallow import Schema, fields, post_load
    import datetime as dt

    class User(object):

        def __init__(self, name, email):
            self.name = name
            self.email = email
            self.created_at = dt.datetime.now()

        def __repr__(self):
            return '<User(name={self.name!r})>'.format(self=self)

    class UserSchema(Schema):

        name = fields.Str()
        email = fields.Email()
        created_at = fields.DateTime()

        @post_load
        def make_user(self, data):
            return User(data['name'], data['email'])

    blackboard = Blackboard(SupportedMemoryType.DICTIONARY)
    blackboard.setup()

    # with marshmallow Scheme, you can also handle complex python objects.
    blackboard.set('user',
        User("G.Ted", "gted221@gmail.com"),
        scheme_cls=UserScheme
    )
    user = blackboard.get('user')
    print(user)
    # <User(name='G.Ted')> will be printed

    # list of complex objects is also supported.
    blackboard.set('users',
        [
            User("User1", "user1@gblackboard.com"),
            User("User2", "user2@gblackboard.com"),
        ],
        scheme_cls=UserScheme
    )
    users = blackboard.get('users')
    print(users)
    # [<User(name='User1')>, <User(name='User2')>] will be printed.


TODO
-------

* Export blackboard in JSON format
* Save blackboard contents
* Validation for Redis configurations
* Print blackboard contents for debugging


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
