from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


from recommender import utils as recommender_utils
from movies.models import Movie


User = get_user_model() # for custom auth


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("count", nargs='?', default=10, type=int)
        parser.add_argument("--movies", action="store_true", default=False)
        parser.add_argument("--users", action="store_true", default=False)
        parser.add_argument("--show-total", action="store_true", default=False)

    def handle(self, *args, **options):
        count = options.get('count')
        show_total = options.get('show_total')
        load_movies = options.get('movies')
        generate_users = options.get('users')

        if load_movies:
            movie_dataset = recommender_utils.load_movie_data(limit=count)
            movies_new = [Movie(**x) for x in movie_dataset]
            movies_bulk = Movie.objects.bulk_create(movies_new, ignore_conflicts=True)
            print(f"New movies {len(movies_bulk)}")
            if show_total:
                print(f"Total movies: {Movie.objects.count()}")

        if generate_users:

            profiles = recommender_utils.get_fake_profiles(count=count)
            new_users = []
            for profile in profiles:
                # User.objects.create(**profile) # this is not efficient
                new_users.append(
                    User(**profile)
                )

            user_bulk = User.objects.bulk_create(new_users, ignore_conflicts=True)
            print(f"New users {len(user_bulk)}")
            if show_total:
                print(f"Total users: {User.objects.count()}")
            # print(f"Hello there are {User.objects.count()} users")