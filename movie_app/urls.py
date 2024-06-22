from django.urls import path

from . import views
app_name = 'movie_app'

urlpatterns=[
    # path('<slug:c_slug>/<slug:movie_slug>/', views.movie_detail, name='movie_category_detail'),
    path('details/<int:id>/', views.details, name="details"),
    path('add_movies/', views.add_movies, name="add_movies"),
    path('edit_movie/<int:id>', views.edit_movie, name="edit_movie"),
    path('delete_movie/<int:id>/', views.delete_movie, name='delete_movie'),
    path('add_review/<int:id>/',views.add_review,name="add_review"),
    path('<slug:c_slug>/', views.movie_display, name='movie_by_category'),
    path('', views.movie_display, name='index'),

]

