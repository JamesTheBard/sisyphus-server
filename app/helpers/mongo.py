from typing import Union

from box import Box
from bson import json_util
from pymongo import MongoClient

from app import mongo
from app.config import Config

db = mongo[Config.MONGO_JOB_DB]


def get_job(job_id: str) -> Union[Box, None]:
    """Get job content from Mongo via `job_id`.

    Args:
        job_id (str): The UUID of the job.

    Returns:
        Union[Box, None]: Returns the content of the job if it exists, None if it does not.
    """
    coll = db[Config.MONGO_JOB_QUEUED]
    post = coll.find_one({"job_id": job_id})
    if not post:
        return None
    post.pop('_id')
    return Box(post)


def post_job(data: Union[Box, dict]) -> None:
    """Post job content to Mongo.

    Args:
        data (Union[Box, dict]): The content of the job to post.
    """
    data = Box(data)
    coll = db[Config.MONGO_JOB_QUEUED]
    print(data.job_id)
    result = coll.replace_one({"job_id": data.job_id}, data, upsert=True)


def delete_queued_jobs() -> None:
    """Delete all jobs information from Mongo.
    """
    coll = db[Config.MONGO_JOB_QUEUED]
    coll.delete_many({})


def delete_job(job_id: str) -> None:
    """Delete job content from Mongo.

    Args:
        job_id (str): The UUID of the job.
    """
    coll = db[Config.MONGO_JOB_QUEUED]
    result = coll.delete_one({"job_id": job_id})
    return bool(result.deleted_count)


def complete_job(job_id: str, is_failed: bool = False) -> bool:
    """Transfer a job to the appropriate collection after processing
    by the worker.

    Args:
        job_id (str): The UUID of the job.
        is_failed (bool, optional): Whether the job failed or not. Defaults to False.

    Returns:
        bool: Whether the job transfered to the appropriate collection successfully.
    """
    dest = "MONGO_JOB_FAILED" if is_failed else "MONGO_JOB_COMPLETED"
    source_coll = db[Config.MONGO_JOB_QUEUED]
    dest_coll = db[getattr(Config, dest)]
    post = source_coll.find_one({"job_id": job_id})
    post.pop('_id')
    result = dest_coll.replace_one({"job_id": job_id}, post, upsert=True)
    if not result.acknowledged:
        return False
    return source_coll.delete_one({"job_id": job_id}).acknowledged
