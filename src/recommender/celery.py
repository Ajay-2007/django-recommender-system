import os


from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "recommender.settings")

app = Celery('recommender')

# CELERY_
app.config_from_object("django.conf:settings", namespace='CELERY')


# app.conf.broker_url = ''
# app.conf.result_backend = 'django-db'
# CELERY_BROKER_URL
app.autodiscover_tasks()