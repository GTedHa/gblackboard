# -*- coding: utf-8 -*-

from gblackboard import Blackboard
from gblackboard import SupportedMemoryType

blackboard = Blackboard(SupportedMemoryType.DICTIONARY)
# Set a key-value data; `set` method should be called only once for a key.
# It's a kind of initialization for data.
blackboard.set('key', 'value')
# Retrieve data with key.
value = blackboard.get('key')
# Update data with new value;
# `update` method should be called after `set` method called for a key.
blackboard.update('key', 'new_value')
# Delete data from blackboard with key.
blackboard.drop('key')
# Clear all data in blackboard.
blackboard.clear()
