import os
import tomllib
from datetime import datetime
from zoneinfo import ZoneInfo

from box import Box

with open('pyproject.toml', 'rb') as f:
    pyproject = Box(tomllib.load(f))

server_tz_info = ZoneInfo(os.environ.get('SERVER_TIMEZONE', "UTC"))


class Config:
    REDIS_URI = os.environ.get(
        "REDIS_URI", "redis://localhost:6379")
    MONGO_URI = os.environ.get(
        "MONGO_URI", "mongodb://root:root@localhost:27017")

    CLIENT_EXIPRY = int(os.environ.get("CLIENT_EXPIRY", "30"))
    SERVER_TIMEZONE = server_tz_info

    MONGO_DATA_DB = os.environ.get("MONGO_DATA_DB", "sisyphus_modules")
    MONGO_DATA_COLL_PREFIX = os.environ.get("MONGO_DATA_COLL_PREFIX", "data_")

    MONGO_JOB_DB = os.environ.get("MONGO_JOB_DB", "sisyphus_jobs")
    MONGO_JOB_FAILED = os.environ.get("MONGO_JOB_COLL_FAILED", "failed")
    MONGO_JOB_COMPLETED = os.environ.get(
        "MONGO_JOB_COLL_COMPLETED", "completed")
    MONGO_JOB_QUEUED = os.environ.get("MONGO_JOB_COLL_QUEUED", "queued")

    VERSION = pyproject.tool.poetry.version
    START_TIME = datetime.now(tz=server_tz_info)

    REDIS_QUEUE_NAME = os.environ.get('REDIS_QUEUE_NAME', 'queue')
    REDIS_WORKER_PREFIX = os.environ.get('REDIS_WORKER_PREFIX', 'worker')
