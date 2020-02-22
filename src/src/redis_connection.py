import os
import redis
redis_connection = redis.Redis(host=os.environ['REDIS_HOST'], port=os.environ['REDIS_PORT'], db=os.environ['REDIS_DB'])