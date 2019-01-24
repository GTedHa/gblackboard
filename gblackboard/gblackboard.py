# -*- coding: utf-8 -*-

from .wrapper import SupportedMemoryType
from .wrapper import DictionaryWrapper, RedisWrapper
from .exception import (
    ExistingKey,
    KeyNotString,
    UnsupportedMemoryType,
    NotCallable,
    NotEditable,
    NonExistingKey
)


class MetaInfo(object):

    def __init__(self, scheme_cls=None, read_only=False):
        self.scheme_cls = scheme_cls
        self.read_only = read_only
        self._callbacks = []

    def add_callback(self, callback):
        if not callable(callback):
            raise NotCallable('Given `callback` function is not callable.')
        self._callbacks.append(callback)

    def callback(self, value):
        for cb in self._callbacks:
            cb(value)

    def remove_callback(self, callback):
        if callback in self._callbacks:
            self._callbacks.remove(callback)

    def clear_callbacks(self):
        del self._callbacks[:]


class Blackboard(object):
    """

    Blackboard class object controls blackboard operations.

    operations: set, get, update, drop, clear values and manage callbacks.

    :param memory_type: Choose memory type between supported memory types (Dictionary, Redis)
    :type memory_type: gblackboard.wrapper.SupportedMemoryType
    :param **kwargs: For Redis configuration. (host, port, db_num, flush, timeout and etc) \n
                     host[string (IP address)] | Redis db host address. default: 'localhost' \n
                     port[integer (0 ~ 65535)] | Redis db port number. default: 6379 \n
                     flush[boolean] | Option to determine whether flush redis db or not after closing this wrapper
                     object. If you set flush=True, only the db which is numbered by db_num is flushed.
                     default: True \n
                     timeout[float >= 0.0] | Timeout for db connection. It would be dangerous if you set timeout as
                     None because the connection attempt between redis client and server can block the whole
                     process. This timeout and socket_timeout option in Redis configuration are same. \n
                     etc | You can set extra redis parameters by kwargs.
                     (e.g. socket_keepalive, socket_keepalive_options, connection_pool, encoding, charset and etc.)
    """

    def __init__(self, memory_type, **kwargs):

        if not SupportedMemoryType.has_value(memory_type):
            raise UnsupportedMemoryType
        self._memory_wrapper = None
        self._memory_type = memory_type
        self._config = {}

        if self._memory_type == SupportedMemoryType.DICTIONARY:
            self._memory_wrapper = DictionaryWrapper()

        elif self._memory_type == SupportedMemoryType.REDIS:
            # redis host config
            if 'host' in kwargs:
                self._config['host'] = kwargs['host']
                del kwargs['host']
            else:
                self._config['host'] = 'localhost'
            # redis port config
            if 'port' in kwargs:
                self._config['port'] = kwargs['port']
                del kwargs['port']
            else:
                self._config['port'] = 6379
            # redis db_num config
            if 'db_num' in kwargs:
                self._config['db_num'] = kwargs['db_num']
                del kwargs['db_num']
            else:
                self._config['db_num'] = 0
            # redis flush (on close) config
            if 'flush' in kwargs:
                self._config['flush'] = kwargs['flush']
                del kwargs['flush']
            else:
                self._config['flush'] = True
            # redis timeout config
            if 'timeout' in kwargs:
                self._config['timeout'] = kwargs['timeout']
                del kwargs['timeout']
                if 'socket_timeout' in kwargs:
                    del kwargs['socket_timeout']
            else:
                self._config['timeout'] = 1.0

            self._memory_wrapper = RedisWrapper(
                host=self._config['host'],
                port=self._config['port'],
                db_num=self._config['db_num'],
                flush=self._config['flush'],
                timeout=self._config['timeout'],
                **kwargs
            )

        self._meta_info = {}

    def setup(self):
        return self._memory_wrapper.setup()

    def close(self):
        del self._meta_info
        self._memory_wrapper.close()

    def set(self, key, value, scheme_cls=None, read_only=False):
        if type(key) is not str:
            raise KeyNotString("Blackboard data `key` should be `str` type.")
        if key in self._meta_info:
            raise ExistingKey("Given `key` already exists in blackboard")
        meta_info = MetaInfo(scheme_cls=scheme_cls, read_only=read_only)
        if scheme_cls:
            if type(value) is list:
                scheme = scheme_cls(strict=True, many=True)
            else:
                scheme = scheme_cls(strict=True)
            value = scheme.dump(value).data  # dump to dictionary
        try:
            success = self._memory_wrapper.set(key, value)
        except Exception:
            raise
        if success:
            self._meta_info[key] = meta_info
        return success

    def get(self, key, json=False):
        if key not in self._meta_info:
            raise NonExistingKey
        meta_info = self._meta_info[key]
        if not json:
            value = self._memory_wrapper.get(key)
            if meta_info.scheme_cls:
                if type(value) is list:
                    scheme = meta_info.scheme_cls(strict=True, many=True)
                else:
                    scheme = meta_info.scheme_cls(strict=True)
                value = scheme.load(value).data
        else:
            value = self._memory_wrapper.get_json_str(key)
        return value

    def update(self, key, value):
        if key not in self._meta_info:
            raise NonExistingKey
        meta_info = self._meta_info[key]
        if meta_info.read_only:
            raise NotEditable("Cannot update read-only data")
        if meta_info.scheme_cls:
            scheme = meta_info.scheme_cls(strict=True)
            _value = scheme.dump(value).data  # dump to dictionary
        else:
            _value = value
        try:
            success = self._memory_wrapper.set(key, _value)
        except Exception:
            raise
        if success:
            meta_info.callback(value)
        return success

    def drop(self, key):
        if key not in self._meta_info:
            raise NonExistingKey
        try:
            success = self._memory_wrapper.delete(key)
        except Exception:
            raise
        if success:
            meta_info = self._meta_info[key]
            meta_info.clear_callbacks()
            del self._meta_info[key]
        return success

    def clear(self):
        keys = self.keys(in_list=True)
        for key in keys:
            self.drop(key)

    def keys(self, in_list=False):
        if in_list:
            return list(self._meta_info.keys())
        return self._meta_info.keys()

    def register_callback(self, key, callback):
        if key not in self._meta_info:
            raise NonExistingKey
        meta_info = self._meta_info[key]
        meta_info.add_callback(callback)
        return id(callback)

    def remove_callback(self, key, callback):
        if key not in self._meta_info:
            raise NonExistingKey
        meta_info = self._meta_info[key]
        meta_info.remove_callback(callback)
        return id(callback)

    def clear_callbacks(self, key):
        if key not in self._meta_info:
            raise NonExistingKey
        meta_info = self._meta_info[key]
        meta_info.clear_callbacks()

    def print_blackboard(self):
        """
        for test
        """
        pass



