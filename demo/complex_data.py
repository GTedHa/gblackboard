# -*- coding: utf-8 -*-

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
