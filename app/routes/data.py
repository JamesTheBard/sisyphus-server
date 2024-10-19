import json

from box import Box
from bson import json_util
from flask import make_response, request
from flask_restx import Resource

from app import api, mongo
from app.config import Config
from app.models.data import modules_data_post

ns = api.namespace('data', description="Data operations")


@ns.route('/<string:module>/<string:name>')
class DataOpsMain(Resource):
    @ns.doc(description="Get data associated with a Sisyphus module")
    @ns.response(200, 'Success')
    @ns.response(404, 'Data Not Found')
    def get(self, module, name):
        db = mongo[Config.MONGO_DATA_DB]
        coll = db[Config.MONGO_DATA_COLL_PREFIX + module]
        post = coll.find_one({"name": name})
        if post == None:
            return None, 404
        response = make_response(json_util.dumps(post), 200)
        response.headers["Content-Type"] = "application/json"
        return response

    @ns.doc(description="Configure data associated with a Sisyphus module")
    @ns.expect(modules_data_post)
    @ns.response(204, 'Data Added')
    def post(self, module, name):
        db = mongo[Config.MONGO_DATA_DB]
        coll = db[Config.MONGO_DATA_COLL_PREFIX + module]
        data = request.get_json()
        data['name'] = name
        result = coll.replace_one({'name': name}, data, upsert=True)
        return None, 204

    @ns.doc(description="Delete data associated with a Sisyphus module")
    @ns.response(204, 'Data Deleted')
    @ns.response(404, 'Data Not Found')
    def delete(self, module, name):
        db = mongo[Config.MONGO_DATA_DB]
        coll = db[Config.MONGO_DATA_COLL_PREFIX + module]
        results = coll.delete_one({"name": name})
        if results.deleted_count:
            return None, 204
        return None, 404
