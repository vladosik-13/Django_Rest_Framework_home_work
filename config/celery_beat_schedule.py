from celery.schedules import crontab

BEAT_SCHEDULE = {
    'example-task-every-minute': {
        'task': 'my_project.tasks.example_task',
        'schedule': crontab(minute='*'),
    },
}