from django.urls import path
from posts.views import create_post,feed,like_post

urlpatterns=[
    path('create_post/',create_post,name="create_post"),
    path('',feed,name="feed"),
    path('like/',like_post,name='like'),
  
]