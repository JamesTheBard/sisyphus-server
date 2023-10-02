from datetime import datetime, timezone

from flask_restx import fields

from app import api

example_task = [
    {
        "module": "ffmpeg",
        "data": {
            "options": {}
        }
    },
    {
        "module": "matroska",
        "data": {
            "more_options": {}
        }
    }
]

queue_attributes_default = {
    'disabled': False,
}

queue_attributes_model = api.model(
    'QueueAttribute', {
        'disabled': fields.Boolean(description='Whether the queue is enabled or disabled', example=False, default=False)
    },
    strict=True
)

job_attributes_model = api.model(
    'JobAttributes', {
        'failed': fields.Boolean(description='Whether the job failed or not.', default=True, example=True),
        'info': fields.Raw(description='Completion information associated with the job.', default=True)
    },
    strict=True
)

tasks_info = api.model('TaskData', {
    'module': fields.String(description='The name of the module to use', required=True),
    'data': fields.Raw(description='The task data to send to the module', required=True),
})

queue_job_post = api.model(
    'QueueJobPost', {
        'job_title': fields.String(description='The title of the job', required=True, example="Awesome Encoder Job"),
        'tasks': fields.List(fields.Nested(tasks_info), description='The task information to use')
    },
    strict=True
)

queue_job_model = api.inherit('QueueJobModel', queue_job_post, {
    'job_id': fields.String(description='The Job ID for the job', example="00000000-1111-2222-3333-444444444444"),
    'added': fields.DateTime(description="The date/time the job was added to the queue", example=str(datetime.now(tz=timezone.utc)))
})

queue_list_model = api.model('QueueJobList', {
    'queue': fields.List(fields.Nested(queue_job_model)),
    'entries': fields.Integer(description='The number of jobs in the queue.', example=1),
    'attributes': fields.Nested(queue_attributes_model)
})

queue_id_model = api.model('QueueID', {
    'job_id': fields.String(description='The job ID associated with the submitted job', example='00000000-1111-2222-3333-444444444444'),
})
