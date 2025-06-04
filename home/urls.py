from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('movie/<int:m>/', views.movie, name='movie'),
    path('search', views.search, name='search'),
    path('addtowatchlist/<int:movie_id>/', views.add_to_watchlist, name='addtowatchlist'),
    path('removefromwatchlist/<int:movie_id>/', views.remove_from_watchlist, name='remove_from_watchlist'),
    path('logout/', views.user_logout, name='user_logout')
   
]