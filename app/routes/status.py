import re
from datetime import datetime

import humanize
from box import Box
from flask_restx import Resource

from app import api
from app.config import Config
from app.models.status import status_config_model

ns = api.namespace('status', description="Server configuration")


def sanitize_uri(uri):
    regex = r'^(\w+:\/\/\w+:)[^@]+(@(\w|\d|\.)+(?::\d+.+)?)$'
    regex = re.compile(regex)
    if match := regex.search(uri):
        return f'{match.group(1)}********{match.group(2)}'
    return uri


@ns.route('/config')
class ServerStatus(Resource):
    @ns.doc(description="Get the current server configuration and run time.")
    @ns.response(200, 'Success', status_config_model)
    def get(self):
        data = Box()
        data.backend = {
            "MONGO_URI": sanitize_uri(Config.MONGO_URI),
            "REDIS_URI": sanitize_uri(Config.REDIS_URI),
        }
        data.version = Config.VERSION
        data.uptime = humanize.naturaldelta(
            datetime.now(tz=Config.SERVER_TIMEZONE) - Config.START_TIME)
        return data, 200


@ns.route('/health')
class HealthCheck(Resource):
    @ns.doc(description="Verify if the server is online.")
    @ns.response(200, 'Success')
    def get(self):
        return {"status": "online"}, 200
