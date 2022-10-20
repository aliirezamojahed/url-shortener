from django.urls import path

from .views import index, shortener_post, shortener, redirect_url

urlpatterns = [
    path('', index, name='index'),
    path('shortener', shortener_post, name='shortener_post'),
    path('shortener/<str:url>', shortener, name='shortener'),
    path('<str:key>', redirect_url, name='redirect')
]