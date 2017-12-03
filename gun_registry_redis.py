from gun_registry import GunRegistry
import redis


class GunRegistryRedis(GunRegistry):
    def __init__(self, ttl=None, **redis_db_params):
        self.ttl = ttl
        self.con = redis.StrictRedis(**redis_db_params)

    def _get_records(self, key):
        self.con.lrange(key, 0, -1)

    def _add_record(self, key, value):
        self.rpush(key, value)
        if self.ttl:
            self.expire(key, self.ttl)
