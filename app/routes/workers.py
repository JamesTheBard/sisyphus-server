import json

from box import Box
from flask import make_response, request
from flask_restx import Resource

from app import api, redis
from app.config import Config
from app.models.workers import workers_disable_model, workers_status_model

ns = api.namespace('worker', description="Worker operations")

r_worker = Config.REDIS_WORKER_PREFIX + '_id:'
r_disabled = Config.REDIS_WORKER_PREFIX + '_disabled:'


@ns.route('/<string:worker_id>')
class WorkerOperations(Resource):
    @ns.doc(description="Get the current status of a worker.")
    @ns.response(200, 'Success', workers_status_model)
    @ns.response(404, 'Worker Not Found')
    def get(self, worker_id):
        if not (content := redis.get(r_worker + worker_id)):
            return None, 404
        return json.loads(content), 200

    @ns.doc(description="Update the current status of a worker.", body=workers_status_model)
    @ns.response(204, 'Worker Updated')
    def post(self, worker_id):
        req = request.get_json()
        content = json.dumps(req, default=str)
        redis.set(r_worker + worker_id, content)
        return None, 204

    @ns.doc(description="Remove the current status of a worker.")
    @ns.response(204, 'Worker Removed')
    @ns.response(404, 'Worker Not Found')
    def delete(self, worker_id):
        if not redis.unlink(r_worker + worker_id):
            return None, 404
        return None, 204


@ns.route('/<string:worker_id>/disable')
class WorkerDisableSettings(Resource):
    @ns.doc(description="Get whether the worker has access to the queue.")
    @ns.response(200, 'Success', workers_disable_model)
    def get(self, worker_id):
        key = r_disabled + worker_id
        if redis.get(key):
            return {"disabled": True}, 200
        return {"disabled": False}, 200

    @ns.doc(description="Disable a worker's access to the queue.")
    @ns.response(204, 'Worker Disabled')
    def post(self, worker_id):
        key = r_disabled + worker_id
        redis.set(key, True)
        return None, 204

    @ns.doc(description="Enable a worker's access to the queue.")
    @ns.response(204, 'Worker Enabled')
    @ns.response(404, 'Worker Not Found')
    def delete(self, worker_id):
        key = r_disabled + worker_id
        if redis.unlink(key):
            return None, 204
        return None, 404
