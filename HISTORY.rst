=======
History
=======

0.1.0 (2019-01-24)
------------------

* First commit on GitHub.


0.1.1 (2019-01-30)
------------------

* Add fakeredis for test


0.2.0 (2019-02-16)
------------------

* Eliminates the limitations of supported data types.
* Change object serialization method for storing data from JSON serialization method using marshmallow (external)
  library to serialization method using pickle library.
* Replace CRUD methods of redis with Hash-CRUD methods
    - set(key, value) -> hset('gblackboard', key, value)
    - get(key)        -> hget('gblackboard', key)
    - delete(key)     -> hdel('gblackboard', key)
    - exists(key)     -> hexists('gblackboard', key)
* Remove useless setup() step and mem_ready status
* Add raise_conn_error (raise 'connection error') decorator for RedisWrapper CRUD methods
* Add save & load features

