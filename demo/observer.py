# -*- coding: utf-8 -*-

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
