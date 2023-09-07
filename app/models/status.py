from flask_restx import fields

from app import api
from app.config import Config

status_config_backend_model = api.model("StatusConfigBackendModel", {
    'MONGO_URI': fields.String(description='The URI of the MongoDB server', example='mongodb://localhost:27017'),
    'REDIS_URI': fields.String(description='The URI of the Redis/KeyDB server', example='redis://localhost:6379'),
})

status_config_model = api.model("StatusConfigModel", {
    'backend': fields.Nested(status_config_backend_model),
    'version': fields.String(description='The current version of the server', example=Config.VERSION),
    'uptime': fields.String(description='Current uptime of the server', example="3 hours"),
})
