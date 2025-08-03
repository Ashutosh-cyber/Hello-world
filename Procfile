web: gunicorn app:app
worker: celery -A automation_scripts worker --loglevel=info
beat: celery -A automation_scripts beat --loglevel=info