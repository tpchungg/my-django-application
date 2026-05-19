from django.urls import path
from . import views

urlpatterns = [
    path('', views.hello, name='hello'),
    path('posts', views.get_posts, name='get_posts'),
    path('metrics', views.metrics, name='metrics'),
]