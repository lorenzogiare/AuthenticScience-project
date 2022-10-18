from django.urls import path
from . import views

urlpatterns = [
    path('articles/', views.article_list, name='article_list'),
    path('articles/<int:pk>/', views.article_details, name='article_details'),
    path('articles/new/', views.new_article, name='new_article'),
    path('articles/<int:pk>/edit/', views.edit_article, name='edit_article'),
    path('author/login/', views.author_login, name='author_login'),
    path('author/registration/', views.author_registration, name='author_registration'),
    path('author/logout/', views.author_logout, name='author_logout'),
    path('articles/<int:pk>/details/', views.details_json, name='details_json'),
]