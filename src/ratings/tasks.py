import random
import time
import datetime

from movies.models import Movie
from django.contrib.auth import get_user_model


from .models import Rating, RatingChoice
from django.contrib.contenttypes.models import ContentType

from celery import shared_task

from django.db.models import Avg, Count
from django.utils import timezone

User = get_user_model()


@shared_task(name='generate_fake_reviews_task')
def generate_fake_reviews(count=100, users=10, null_avg=False):
    user_s = User.objects.first() # 1
    user_e = User.objects.last() # ??
    random_user_ids = random.sample(range(user_s.id, user_e.id), users)

    users = User.objects.filter(id__in=random_user_ids)
    # users = User.objects.all().order_by("?")[:users]
    movies = Movie.objects.all().order_by("?")[:count]
    # movie_ctype = ContentType.objects.get_for_model(Movie)

    if null_avg:
        movies = Movie.objects.filter(rating_avg__isnull=True).order_by("?")[:count]

    n_ratings = movies.count()
    rating_choices = [x for x in RatingChoice.values if x is not None] # 1, 2, 3, 4, 5
    user_ratings = [random.choice(rating_choices) for _ in range(0, n_ratings)]

    new_ratings = []

    for movie in movies:
        rating_obj = Rating.objects.create(
            content_object=movie,
            # content_type=movie_ctype,
            # object_id=movie.id,
            value=user_ratings.pop(),
            user=random.choice(users)
        )
        new_ratings.append(rating_obj.id)

    return new_ratings


@shared_task(name='task_update_movie_ratings')
def task_update_movie_ratings(object_id=None):
    start_time = time.time()
    ctype = ContentType.objects.get_for_model(Movie)

    rating_qs = Rating.objects.filter(content_type=ctype)
    # ratings = Rating.objects.all().values('object_id').annotate(average=Avg('value')) # this will give me all of the object_id inside of ratings


    if object_id is not None:
        rating_qs = rating_qs.filter(object_id=object_id)

    agg_ratings = rating_qs.values('object_id').annotate(average=Avg('value'), count=Count('object_id')) # this gives me all of the ratings for all of the movies combined together
    for agg_rate in agg_ratings:
        object_id = agg_rate['object_id']
        rating_avg = agg_rate['average']
        rating_count = agg_rate['count']
        qs = Movie.objects.filter(id=object_id)
        qs.update(
            rating_avg=rating_avg,
            rating_count=rating_count,
            rating_last_updated=timezone.now()
        )
    total_time = time.time() - start_time
    delta = datetime.timedelta(seconds=int(total_time))
    print(f"Rating update took {delta} ({total_time}s)")

