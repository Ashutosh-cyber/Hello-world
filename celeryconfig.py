import os
from dotenv import load_dotenv

load_dotenv()

# Broker settings
broker_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
result_backend = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

# Task settings
task_serializer = 'json'
accept_content = ['json']
result_serializer = 'json'
timezone = 'UTC'
enable_utc = True

# Task routing
task_routes = {
    'automation_scripts.send_followup_message': {'queue': 'messages'},
    'automation_scripts.check_form_dropoffs': {'queue': 'monitoring'},
    'automation_scripts.check_recommendation_followups': {'queue': 'monitoring'},
    'automation_scripts.generate_daily_report': {'queue': 'reports'},
    'automation_scripts.cleanup_old_sessions': {'queue': 'maintenance'},
}

# Worker settings
worker_prefetch_multiplier = 1
task_acks_late = True
worker_max_tasks_per_child = 1000

# Beat schedule (periodic tasks)
beat_schedule = {
    'check-form-dropoffs': {
        'task': 'automation_scripts.check_form_dropoffs',
        'schedule': 3600.0,  # Every hour
    },
    'check-recommendation-followups': {
        'task': 'automation_scripts.check_recommendation_followups',
        'schedule': 3600.0,  # Every hour
    },
    'generate-daily-report': {
        'task': 'automation_scripts.generate_daily_report',
        'schedule': 86400.0,  # Daily
    },
    'cleanup-old-sessions': {
        'task': 'automation_scripts.cleanup_old_sessions',
        'schedule': 86400.0,  # Daily
    },
}

# Result backend settings
result_expires = 3600  # 1 hour

# Task execution settings
task_time_limit = 300  # 5 minutes
task_soft_time_limit = 240  # 4 minutes

# Retry settings
task_retry_delay = 60  # 1 minute
task_max_retries = 3