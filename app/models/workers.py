from flask_restx import fields

from app import api

workers_attributes_default = {
    'disabled': False
}

workers_attributes_model = api.model(
    'WorkerAttributes', {
        'disabled': fields.Boolean(description="Whether the worker is disabled or not."),
    },
    strict=True,
)

workers_status_post = api.model(
    'WorkerStatusPost', {
        'status': fields.String(description='The current status of the worker.', required=True, example="in_progress"),
        'online_at': fields.String(description='The start time of the worker.', required=True),
        'hostname': fields.String(description='The hostname of the worker.', required=True, example="encoder01"),
        'version': fields.String(description='The version of Sisyphus running on the worker.', required=True, version="1.0.0"),
        'task': fields.String(description='The module being run on the worker.', example="ffmpeg"),
        'job_id': fields.String(description='The ID of the job being run.', example="00000000-1111-2222-3333-444444444444"),
        'job_title': fields.String(description='The title of the job being run.', example='Awesome Encoding Job'),
        'progress': fields.Float(description='The progress of the current task.', example=3.74),
        'info': fields.Raw(description='Additional information from the worker'),
    },
    strict=True
)

workers_status_model = api.inherit('WorkerStatusModel', workers_status_post, {
    'attributes': fields.Nested(workers_attributes_model),
    'worker_id': fields.String(description='The UUID of the worker')
})

workers_data_model = api.model('WorkerDataPost', {})

workers_disable_model = api.model('WorkerDisabled', {
    'disabled': fields.Boolean(description='The state of the worker with respect to accessing the queue')
})

workers_model = api.model('WorkersModel', {
    'workers': fields.List(fields.Nested(workers_status_model)),
    'count': fields.Integer(description="The number of workers online.")
})
