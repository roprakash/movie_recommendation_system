from .models import Movie, Genre, Rating


# to list movies like the given movie based on the genres ordered by rating
def order_by_rating(res):
    res = sorted(res, key= lambda x: x.avg_rate, reverse = True)
    return res


def get_similar_movies(movie):
    res = []
    given_movie = set()
    given_movie.add(movie)
    for i in movie.genres.all():                    
        res.extend(set(i.has_movies.all()).difference(given_movie))                             # try to order by rating
    res = set(res)
    return order_by_rating(res)


def popular_genres(popular):
    popular_genres = set()
    for i in popular:
        for j in i.genres.all():
            popular_genres.add(j)
    # print(popular_genres)
    picked_genres = {}
    for i in popular_genres:
        picked_genres[i.genre] = set(i.has_movies.all())
    return picked_genres


def get_movies_based_rating(request, rated_movies):
    fav_genres = set()
    fav_movies = set()
    based_rating = []
    for i in Movie.objects.raw(f"select * from mrs_movie m where id in (select movie_id from mrs_rating r where r.user_id ={request.user.id} and r.rate>=3)"):
        fav_movies.add(i)
    for j in fav_movies:
        for k in j.genres.all():
            fav_genres.add(k.id)
    fav_genres = tuple(fav_genres)
    
    # to list movies based on user's fav genres
    for i in fav_genres:
        movies_in_genre = Genre.objects.get(id=i)
        based_rating.extend(movies_in_genre.has_movies.all())
    based_rating = set(based_rating).difference(rated_movies)
    
    based_rating = order_by_rating(based_rating)
    return based_rating
