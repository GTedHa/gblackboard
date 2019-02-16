=====
Usage
=====

To use gblackboard in a project:

- basic usage::

.. code-block:: python

    from gblackboard import Blackboard
    from gblackboard import SupportedMemoryType

    blackboard = Blackboard(SupportedMemoryType.DICTIONARY)
    # Set a key-value data;
    # `set` method should be called only once for a key.
    # It's a kind of initialization for data.
    blackboard.set('key', 'value')
    # Retrieve data with key.
    value = blackboard.get('key')
    # Update data with new value;
    # `update` method should be called
    # after `set` method called for a key.
    blackboard.update('key', 'new_value')
    # Delete data from blackboard with key.
    blackboard.drop('key')
    # Clear all data in blackboard.
    blackboard.clear()


- observer::

.. code-block:: python

    from gblackboard import Blackboard
    from gblackboard import SupportedMemoryType

    def callback(data):
        print(data)

    blackboard = Blackboard(SupportedMemoryType.DICTIONARY)
    blackboard.set('key', 'value')
    # Register `callback` function as a callback.
    blackboard.register_callback('key', callback)
    # Update data;
    # `callback` function will be called during `update`,
    # and `new_value` will passed to `callback` function.
    blackboard.update('key', 'new_value')


- complex data::

.. code-block:: python

    from gblackboard import Blackboard
    from gblackboard import SupportedMemoryType

    import datetime as dt

    class User(object):

        def __init__(self, name, email):
            self.name = name
            self.email = email
            self.created_at = dt.datetime.now()

        def __repr__(self):
            return '<User(name={self.name!r})>'.format(self=self)

    blackboard = Blackboard(SupportedMemoryType.DICTIONARY)

    # You can also store customized class objects in blackboard.
    blackboard.set('user', User("G.Ted", "gted221@gmail.com"))
    user = blackboard.get('user')
    print(user)
    # <User(name='G.Ted')> will be printed.

    # List of complex objects is also supported.
    blackboard.set('users',
        [
            User("User1", "user1@gblackboard.com"),
            User("User2", "user2@gblackboard.com"),
        ]
    )
    users = blackboard.get('users')
    print(users)
    # [<User(name='User1')>, <User(name='User2')>] will be printed.


- save & load::

.. code-block:: python

    from gblackboard import Blackboard
    from gblackboard import SupportedMemoryType

    import datetime as dt

    class User(object):

        def __init__(self, name, email):
            self.name = name
            self.email = email
            self.created_at = dt.datetime.now()

        def __repr__(self):
            return '<User(name={self.name!r})>'.format(self=self)

    blackboard = Blackboard(SupportedMemoryType.DICTIONARY)
    # Store sample data
    blackboard.set('user', User("G.Ted", "gted221@gmail.com"))
    # Save current blackboard contents as file.
    blackboard.save()
    # Close current blackboard;
    # this means clear all data in blackboard
    blackboard.close()
    # ------------------------------------------------------------
    blackboard = Blackboard(SupportedMemoryType.DICTIONARY)
    # Load saved blackboard contents from files.
    blackboard.load()
    user = blackboard.get('user')
    print(user)
    # <User(name='G.Ted')> will be printed.
