from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_search_history, name='search_history'),
]