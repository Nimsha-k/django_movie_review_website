from django.urls import path
from . import views

app_name='search_app'
urlpatterns=[
    path('search_results/',views. search_results,name='search_results'),
]
