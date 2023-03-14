from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from ratings.models import Rating

from django.utils import timezone
import datetime

RATING_CALC_TIME = 1

class Movie(models.Model):
    title = models.CharField(max_length=120, unique=True)
    overview = models.TextField()
    release_date = models.DateField(blank=True, null=True, auto_now=False, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    ratings = GenericRelation(Rating) # queryset # user.rating_set.all()
    rating_last_updated = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    rating_count = models.IntegerField(blank=True, null=True)
    rating_avg = models.DecimalField(decimal_places=2, max_digits=5, blank=True, null=True) # 5.00, 0.00


    def rating_avg_display(self):
        now = timezone.now()

        if not self.rating_last_updated:
            return self.calculate_rating()


        if self.rating_last_updated > now - datetime.timedelta(minutes=RATING_CALC_TIME):
            return self.rating_avg

        return self.calculate_rating()

    def calculate_ratings_count(self):
        return self.ratings.all().count()


    def calculate_ratings_avg(self):
        return self.ratings.avg()


    def calculate_rating(self, save=True):
        rating_avg = self.calculate_ratings_avg()
        rating_count = self.calculate_ratings_count()
        self.rating_count = rating_count
        self.rating_avg = rating_avg
        self.rating_last_updated = timezone.now()
        if save:
            self.save()

        return self.rating_avg


