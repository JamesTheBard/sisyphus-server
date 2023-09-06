from datetime import datetime

from pymongo import MongoClient
import redis as r
from flask import Flask
from flask_restx import Api, Resource

from app.config import Config

app = Flask(__name__)
api = Api(app, doc="/doc/")

redis = r.from_url(Config.REDIS_URI)
mongo = MongoClient(Config.MONGO_URI)

from app.routes import status, queue, workers, data
