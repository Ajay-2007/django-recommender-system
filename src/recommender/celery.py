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

app.conf.beat_schedule = {
    "run_movie_rating_avg_every_30": {
        # 'task': 'movie.tasks.task_calculate_movie_ratings', # if we haven't given a name
        'task': 'task_calculate_movie_ratings',
        'schedule': 60 * 30, # 30 min, schedule in seconds
        'kwargs': {"count": 20_000}
    }
}