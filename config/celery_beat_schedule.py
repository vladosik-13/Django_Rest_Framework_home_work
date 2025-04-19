from celery.schedules import crontab

BEAT_SCHEDULE = {
    "example-task-every-minute": {
        "task": "my_project.tasks.example_task",
        "schedule": crontab(minute="*"),
    },
    "deactivate-inactive-users-every-day": {
        "task": "users.tasks.deactivate_inactive_users",
        "schedule": crontab(hour=0, minute=0),  # Каждый день в полночь
    },
}
