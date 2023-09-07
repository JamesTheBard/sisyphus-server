from datetime import datetime

from flask_restx import fields

from app import api

example_task = {
    "ffmpeg": {
        "options": {}
    },
    "matroska": {
        "more_options": {}
    }
}

queue_attributes_default = {
    'disabled': False,
}

queue_attributes_model = api.model(
    'QueueAttribute', {
        'disabled': fields.Boolean(description='Whether the queue is enabled or disabled', example=False, default=False)
    },
    strict=True
)

queue_job_post = api.model('QueueJobPost', {
    'job_title': fields.String(description='The title of the job', required=True, example="Awesome Encoder Job"),
    'tasks': fields.List(fields.Raw, description='The tasks associated with the job', required=True, example=example_task),
})

queue_job_model = api.model('QueueJobModel', {
    'job_title': fields.String(description='The title of the job', example="Awesome Encoder Job"),
    'job_id': fields.String(description='The Job ID for the job', example="00000000-1111-2222-3333-444444444444"),
    'tasks': fields.List(fields.Raw, description='The tasks associated with the job', example=example_task),
    'added': fields.DateTime(description="The date/time the job was added to the queue", example=str(datetime.utcnow()))
})

queue_list_model = api.model('QueueJobList', {
    'queue': fields.List(fields.Nested(queue_job_model)),
    'entries': fields.Integer(description='The number of jobs in the queue.', example=1),
    'attributes': fields.Nested(queue_attributes_model)
})

queue_id_model = api.model('QueueID', {
    'job_id': fields.String(description='The job ID associated with the submitted job', example='00000000-1111-2222-3333-444444444444'),
})
