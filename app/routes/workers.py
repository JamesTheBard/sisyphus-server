import json

from box import Box
from flask import make_response, request
from flask_restx import Resource

from app import api, redis
from app.config import Config
from app.models.workers import (workers_attributes_default,
                                workers_attributes_model, workers_model,
                                workers_status_model, workers_status_post)

ns = api.namespace('workers', description="Worker operations")

r_worker = Config.REDIS_WORKER_PREFIX + '_id:'
r_attributes = Config.REDIS_WORKER_PREFIX + '_attributes:'


@ns.route('')
class WorkersOperations(Resource):
    @ns.doc(description="Get all online workers.")
    @ns.response(200, 'Success', workers_model)
    def get(self):
        response = Box()
        keys = redis.keys(r_worker + '*')
        response.workers = [i.decode().split(':')[-1]
                            for i in redis.keys(r_worker + '*')]
        response.count = len(response.workers)
        return response, 200


@ns.route('/<string:worker_id>')
class WorkerOperations(Resource):
    @ns.doc(description="Get the current status of a worker.")
    @ns.response(200, 'Success', workers_status_model)
    @ns.response(404, 'Worker Not Found')
    def get(self, worker_id):
        if not (content := redis.get(r_worker + worker_id)):
            return None, 404
        content = Box(json.loads(content))
        key = r_attributes + worker_id
        if not (attributes := redis.get(key)):
            attributes = json.dumps(workers_attributes_default, default=str)
            redis.set(key, attributes)
        content.attributes = json.loads(attributes)
        return content, 200

    @ns.doc(description="Update the current status of a worker.")
    @ns.expect(workers_status_post, validate=True)
    @ns.response(204, 'Worker Updated')
    def post(self, worker_id):
        req = request.get_json()
        content = json.dumps(req, default=str)
        redis.set(r_worker + worker_id, content)
        return None, 204

    @ns.doc(description="Update the attributes of a worker.")
    @ns.expect(workers_attributes_model, validate=True)
    @ns.response(204, 'Worker Attributes Updated')
    @ns.response(400, 'Bad Request')
    def patch(self, worker_id):
        key = r_attributes + worker_id
        req = request.get_json()
        attributes = json.loads(redis.get(key))
        for k, v in req.items():
            attributes[k] = v
        redis.set(key, json.dumps(attributes, default=str))
        return None, 204

    @ns.doc(description="Remove the current status of a worker.")
    @ns.response(204, 'Worker Removed')
    @ns.response(404, 'Worker Not Found')
    def delete(self, worker_id):
        if not redis.unlink(r_worker + worker_id):
            return None, 404
        return None, 204
