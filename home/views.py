from django.shortcuts import render
from django.http import HttpResponseRedirect
import tmdbsimple as t
from django.views.decorators.http import require_POST
from django.shortcuts import redirect
from .models import Watchlist
from django.contrib.auth import logout


from .models import LikedMovie
import random
from django.core.cache import cache

import logging

logger = logging.getLogger(__name__)


t.API_KEY = '2c5736d962193d3e5f4a4106a59691c7'



def home(r):
    pickup_lines = [
        "Are you a plot twist? Because you just made my story interesting.",
        "If we were in a movie, you'd be my favorite scene.",
        "Are you a rom-com? Because my heart skips a beat every time I see you.",
        "If you were a movie, you'd be a box office hit in my heart.",
        "Are you the end credits? Because I never want this moment to end.",
        "You must be a director, because you just called 'action' on my feelings.",
        "Is your name IMDb? Because you just rated my day a perfect 10.",
        "Are you a sequel? Because I want to see you again and again.",
        "Are you a popcorn bucket? Because I can't watch a movie without you."
    ]

    pickup_line = random.choice(pickup_lines)

    if r.user.is_authenticated:
        cache_key = f'recommendations_{r.user.id}'
        data = cache.get(cache_key)

       
        movie_ids = Watchlist.objects.filter(user=r.user).values_list('movie', flat=True)

       
        watchlist_movies = []
        for movie_id in movie_ids:
            try:
                movie = t.Movies(movie_id)
                movie_info = movie.info()
                watchlist_movies.append(movie_info)
            except Exception as e:
                print(f"TMDb error for movie ID {movie_id}: {e}")

       
        recommended_movies = []
        seen_ids = set(movie_ids)  
        for movie_id in movie_ids:
            try:
                movie = t.Movies(movie_id)
                similar = movie.similar_movies()['results']
                for sim in similar[:3]:  
                    if sim['id'] not in seen_ids:
                        recommended_movies.append(sim)
                        seen_ids.add(sim['id'])
            except Exception as e:
                print(f"Error fetching similar movies for ID {movie_id}: {e}")

        recommendations_ready = True

        # Get popular movies
        try:
            popular = t.Movies().popular()
            popular_movies = popular.get('results', [])[:10]
        except Exception as e:
            print(f"Error fetching popular movies: {e}")
            popular_movies = []

        return render(r, 'home.html', {
            'recommended_movies': recommended_movies,
            'watchlist_movies': watchlist_movies,
            'popular_movies': popular_movies,
            'pickup_line': pickup_line,
            'recommendations_ready': recommendations_ready,
        })

    else:
        return HttpResponseRedirect('/login/')
    
def movie(r,m):
    if r.user.is_authenticated:
        movie = t.Movies(m).info()
        return render(
            r,
            'movie.html',
            {
                'username': r.user.username,
                'movie': movie
            }
        )
    else:
        return HttpResponseRedirect('/login/')

def search(request):
     
    if not request.user.is_authenticated:
        return redirect('login')

    query = request.GET.get('query', '').strip()
    results = []

    if query:
        try:
            search_obj = t.Search()
            response = search_obj.movie(query=query)
            results = response.get('results', [])
            logger.info(f"Search successful for query: {query}, results found: {len(results)}")
        except Exception as e:
            logger.error(f"Error during TMDb search: {e}")
            results = []

    return render(request, 'search.html', {
        'username': request.user.username,
        'search_results': results,
        'query': query,
    })

@require_POST
def add_to_watchlist(request, movie_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')
    try:
        Watchlist.objects.get_or_create(user=request.user, movie=movie_id)
    except Exception as e:
        print(f"Error adding to watchlist: {e}")
    return redirect('home')

@require_POST
def remove_from_watchlist(request, movie_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')
    Watchlist.objects.filter(user=request.user, movie=movie_id).delete()
    return redirect('home')

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')

