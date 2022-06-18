CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://scavenger-redis-master:6379",
        "TIMEOUT": 45,
    },
    "renditions": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": ["redis://scavenger-redis-master:6379", "redis://scavenger-redis-replicas:6379"],
        "TIMEOUT": 86_400,
    },
}
