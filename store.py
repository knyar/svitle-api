import logging

from redis import BlockingConnectionPool
from redis.client import Redis
from redis.exceptions import RedisError 

import config
import models

class Store:
    def __init__(self, redis_url, keep_last=10):
        logging.info("Connecting to redis at %s", redis_url)
        self._redis = Redis(
            socket_timeout=5, socket_connect_timeout=5,
            health_check_interval=2,
            connection_pool=BlockingConnectionPool.from_url(redis_url))
        self._last_id = keep_last-1

    def add_stream_info(self, station: str, stream: models.StreamInfo):
        try:
            self._redis.lpush(self._list_key(station), stream.to_json())
            self._redis.ltrim(self._list_key(station), 0, self._last_id)
        except RedisError as e:
            logging.error("add_stream_info error: %s", e)

    def get_history(self, station: str, count=None):
        lst = 'svitle:history:%s' % station
        last_id = self._last_id if not count else count-1
        try:
            resp = self._redis.lrange(self._list_key(station), 0, last_id)
            return [models.StreamInfo.from_json(m) for m in resp]
        except RedisError as e:
            logging.error("get_history error: %s", e) 
            return []

    def _list_key(self, station: str) -> str:
        return '{}:history:{}'.format(config.redis_key_prefix, station)