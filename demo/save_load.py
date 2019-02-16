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
