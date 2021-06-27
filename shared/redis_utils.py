import redis
from dynaconf import settings as dyna_settings


class RedisUtil:
    redis_url = f"redis://{dyna_settings.REDIS_ADDRESS}"
    pool = redis.ConnectionPool.from_url(redis_url)
    client = redis.Redis(connection_pool=pool)

    @classmethod
    def set_key(cls, key, *, value, ex_time=30 * 60):
        """ 设置一个key """
        cls.client.set(key, value, ex_time)

    @classmethod
    def get_key(cls, key):
        """ 获取一个key """
        res = cls.client.get(key)
        return res.decode() if res else res

    @classmethod
    def delete_key(cls, key):
        cls.client.delete(key)
