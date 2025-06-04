from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin




class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchlist')
    movie = models.IntegerField()
   
class LikedMovie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked_movies')
    movie = models.IntegerField()

    
    

admin.site.register(LikedMovie)