from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError

from .models import Movie, Genre, Rating
from .utils import *
        
        
def home(request):
    recent = Movie.objects.raw("select * from mrs_movie order by year desc, mth desc limit 6") 
    popular = Movie.objects.raw("select * from mrs_movie order by avg_rate desc limit 6")
    
    
    # to list movies like the 1st movie in the most popular list
    top_pick = set()
    top_pick.add(popular[0])
    like_top_pick = get_similar_movies(popular[0])
    
    # dictionary of picked genres and movies based on popular movies
    picked_genres = popular_genres(popular)
    # print("dict", picked_genres)
    
    if request.user.is_authenticated:    
        # to list fav genres of user
        rated_movies = Movie.objects.raw(f"select * from mrs_movie m where id in (select movie_id from mrs_rating r where r.user_id ={request.user.id} order by r.rate desc)")
        
        # to list movies based on user rated movies where user rating is > 3
        based_rating = get_movies_based_rating(request, rated_movies)
        if len(rated_movies) == 0:
            based_rating = None
            rated_movies = None
        
        # print(based_rating)
        # print(fav_movies)
        
        return render(request, 'mrs/home.html', {
            "recent": recent,
            "popular": popular,
            "top_pick": popular[0],
            "like_top_pick": like_top_pick,
            "picked_genres": picked_genres,
            
            "based_ratings": based_rating,
            "watched": rated_movies,
            })
    else:
        
        return render(request, 'mrs/home.html', {
            "recent": recent,
            "popular": popular,
            "top_pick": popular[0],
            "like_top_pick": like_top_pick,
            "picked_genres": picked_genres,
            })


@login_required
def logoutuser(request):
    if request.method == "POST":
        logout(request)
        return redirect('home')

    
def signupuser(request) :
    if request.method == 'GET':    
        return render(request, 'mrs/signupuser.html', {
            'form': UserCreationForm()
        })
    else :
        if request.POST['password1'] == request.POST['password2'] :
            try :
                user = User.objects.create_user(request.POST['username'], password = request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError :
                return render(request, 'mrs/signupuser.html', {
                    'error': 'That Username already exists'
                })

        else :
            return render(request, 'mrs/signupuser.html', {
                'form': UserCreationForm(), 'error': 'Passwords did not match'
            })


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'mrs/loginuser.html')
    else:
        if request.POST['username'] == '' or request.POST['password'] == '':
            return render(request, 'mrs/loginuser.html', {
                'error': 'Fill the details'
            })
        else:
            user = authenticate(request, username=request.POST["username"], password=request.POST["password"])
            if user is None:
                return render(request, 'mrs/loginuser.html', {
                    'error': 'Username and password did not match'
                })
            else:
                login(request, user)
                return redirect('home')  

            
def watch_movie(request, movie_pk):
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    
    movie = get_object_or_404(Movie, pk=movie_pk)
    similar_movies = get_similar_movies(movie)
    
    if request.method == 'GET':
        
        try:
            rating = Rating.objects.get(movie = movie, user = request.user)
            rate = rating.rate
        except:
            rate = None
            
        # print(rate, request.user)   
        return render(request, 'mrs/watch_movie.html', {
            "movie": movie,
            "rating": rate,
            "month": months[movie.mth-1],
            "similar": similar_movies,
        })
    else:
        rate = None
        if request.user.is_authenticated:
            rate = request.POST.get('rate')
            rate = int(rate)
            
            rating = Rating(movie = movie, user = request.user, rate = rate)
            rating.save()
            
            # movie.no_votes += len(Rating.objects.raw(f"select * from mrs_rating where movie_id={movie.id}"))
            # for i in  Rating.objects.raw(f"select * from mrs_rating where movie_id={movie.id}"):
            #     tot += i.rate
            # movie.avg_rate += tot_rate/movie.no_votes
            
            movie.no_votes += 1
            movie.avg_rate = round((movie.avg_rate + rate)/2, 2)
            movie.save()
            # print(rate, rating.user)
            return redirect("home")
        else:
            return render(request, 'mrs/watch_movie.html', {
                "movie": movie,
                "rating": rate,
                "month": months[movie.mth-1],
                "similar": similar_movies,
                "error": "Login Required!"
            })


def all_movies(request):
    all_movies = Movie.objects.raw("select * from mrs_movie order by year desc, mth desc") 
    movies_by_year = {}
    no_movies = len(all_movies)
    for i in all_movies:
        if i.year not in movies_by_year:
            movies_by_year[i.year] = set()
            movies_by_year[i.year].add(i)
        else:
            movies_by_year[i.year].add(i)
            
    return render(request, "mrs/all_movies.html", {
        "movies_by_year": movies_by_year,
        "no_movies": no_movies
    })