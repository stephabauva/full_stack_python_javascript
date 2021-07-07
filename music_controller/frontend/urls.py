from django.urls import path
from .views import index


app_name = 'frontend' 
# this is so django knows that this urls.py belongs to the frontend app
# it is required to make the 'redirect' of spotify_callback (views) work 

urlpatterns = [
    path('', index, name=''), 
    # naming the path (name='') is necessary to identifying the path so that when we call 
    # the redirect function, we know which path we should actually go to
    path('join', index),
    path('create', index),
    path('room/<str:roomCode>', index),
    path('info', index),
]
