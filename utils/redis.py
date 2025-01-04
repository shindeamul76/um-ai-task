
from django.conf import settings
import redis



redis_client = redis.Redis(
    host=settings.LOGS_REDIS['HOST'],
    port=settings.LOGS_REDIS['PORT'],
    password=settings.LOGS_REDIS['PASSWORD'],
    decode_responses=True
)