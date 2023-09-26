from datetime import datetime

from pymongo import MongoClient
import redis as r
import logging
from flask import Flask
from flask_restx import Api, Resource
from flask_cors import CORS

from app.config import Config

app = Flask(__name__)
cors = CORS(app)
app.logger.setLevel(logging.INFO)
api = Api(app, doc="/doc/")

redis = r.from_url(Config.REDIS_URI)
mongo = MongoClient(Config.MONGO_URI)

from app.routes import status, queue, workers, data
