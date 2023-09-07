import json
import uuid
from datetime import datetime
from box import Box
from flask import request
from flask_restx import Resource

from app import api, redis, Config
from app.models.queue import queue_job_post, queue_list_model, queue_job_model, queue_id_model, queue_attributes_model, queue_attributes_default
from app.models.workers import workers_disable_model

queue_ns = api.namespace('queue', description="Queue operations")
job_ns = api.namespace('jobs', description="Job operations")

r_queue = Config.REDIS_QUEUE_PREFIX
r_queue_attributes = r_queue + '_attributes'
r_key = r_queue + '_id:'


@queue_ns.route('')
class QueueMain(Resource):
    @queue_ns.doc(description="Get all jobs on the current queue.")
    @queue_ns.response(200, 'Success', queue_list_model)
    def get(self):
        queue = [json.loads(redis.get(r_key + i.decode())) for i in reversed(
            redis.lrange("queue", 0, -1))]
        if not (attributes := redis.get(r_queue_attributes)):
            attributes = json.dumps(queue_attributes_default, default=str)
            redis.set(r_queue_attributes, attributes)
        return {'queue': queue, 'entries': len(queue), 'attributes': json.loads(attributes)}, 200

    @queue_ns.doc(body=queue_job_post, description="Add a job to the end of the current queue.")
    @queue_ns.response(200, 'Success', queue_id_model)
    def post(self):
        job_id = str(uuid.uuid4())
        req = Box(request.get_json())
        req.job_id = job_id
        req.added = datetime.utcnow()
        content = json.dumps(req, default=str)
        redis.lpush(r_queue, job_id)
        redis.set(r_key + job_id, content)
        return {'job_id': job_id}, 200

    @queue_ns.doc(description="Change the attributes of the queue.")
    @queue_ns.expect(queue_attributes_model, validate=True)
    @queue_ns.response(204, 'Updated Successfully')
    @queue_ns.response(400, 'Bad Request')
    def patch(self):
        req = Box(request.get_json())
        attributes = json.loads(redis.get(r_queue_attributes))
        for k, v in req.items():
            attributes[k] = v
        redis.set(r_queue_attributes, json.dumps(attributes, default=str))
        return None, 204

    @queue_ns.doc(description="Clear all jobs from the queue.")
    @queue_ns.response(204, 'Queue Cleared')
    def delete(self):
        redis.delete(r_queue)
        for k in redis.scan_iter(r_key + '*', count=500):
            redis.unlink(k)
        return None, 204


@queue_ns.route('/poll')
class PollQueue(Resource):
    @queue_ns.doc(description="Removes a job from the queue for processing")
    @queue_ns.response(200, 'Success', queue_job_model)
    @queue_ns.response(404, 'Queue is Empty')
    def get(self):
        if not (job_id := redis.rpop(r_queue).decode()):
            return None, 404
        content = redis.get(r_key + job_id)
        redis.unlink(r_key + job_id)
        return json.loads(content), 200


@job_ns.route('/<string:job_id>')
class JobMain(Resource):
    @job_ns.doc(description="The details for a given job via its ID")
    @job_ns.response(200, 'Success', queue_job_model)
    @job_ns.response(404, 'Job ID Not Found')
    def get(self, job_id):
        if not (content := redis.get(r_key + job_id)):
            return None, 404
        return json.loads(content), 200

    @job_ns.doc(description="Remove a job from the queue")
    @job_ns.response(204, 'Job Removed')
    @job_ns.response(404, 'Job ID Not Found')
    def delete(self, job_id):
        if not redis.unlink(r_key + job_id):
            return None, 404
        redis.lrem('queue', count=0, value=job_id)
        return None, 204
