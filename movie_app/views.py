from django.contrib import messages
from django.db.models import Avg
from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Movies, Review
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from .forms import MovieForm, ReviewForm


# Create your views here.
def movie_display(request, c_slug=None):
    c_page = None
    movie_list = None
    categories = Category.objects.all()
    if c_slug != None:
        c_page = get_object_or_404(Category, slug=c_slug)
        movie_list = Movies.objects.all().filter(category=c_page, available=True)
    else:
        movie_list = Movies.objects.all().filter(available=True)
    paginator = Paginator(movie_list, 8)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1
    try:
        movies = paginator.page(page)
    except (EmptyPage, InvalidPage):
        movies = paginator.page(paginator.num_pages)
    return render(request, "index.html", {'category': c_page, 'movies': movies, 'links': categories})





def add_movies(request):
    if request.user.is_authenticated:  # Check if the user is authenticated
        if request.method == "POST":
            form = MovieForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, "Movie added successfully!")
                return redirect('movie_app:index')  # Redirect to the index page after adding movie
        else:
            form = MovieForm()
        return render(request, "add_movie.html", {'form': form, 'controller': 'Add Movies'})
    else:
        return redirect('accounts:login')  # Redirect to the login page if the user is not authenticated

def details(request, id):

     movies = get_object_or_404(Movies, id=id)
     reviews=Review.objects.filter(movies=movies.id).order_by("-comment")
     average=reviews.aggregate(Avg("rating"))["rating__avg"]
     if average == None:
         average=0
     average=round(average,2)
     return render(request, "movie_detail.html",{'movies': movies,'reviews':reviews,'average':average} )



def edit_movie(request,id):
    if request.user.is_authenticated:
        movies=Movies.objects.get(id=id)
        if request.user == movies.user or request.user.is_staff:
            form=MovieForm(request.POST or None, request.FILES,instance=movies)
            if form.is_valid():
                form.save()
                return redirect('movie_app:details',id)
            else:
                form=MovieForm(instance=movies)
            return render(request,'add_movie.html',{'form':form,'controller':'Edit Movies'})
    # if they are not user
        else:
            print("You can't edit this movie the movie")
            return redirect('movie_app:index')
    else:
        print("User is not authenticated")
        return redirect("accounts:login")

def delete_movie(request,id):
    if request.user.is_authenticated:
         movies=Movies.objects.get(id=id)
         if request.user == movies.user or request.user.is_staff:
            movies.delete()
            return redirect('movie_app:index')
         else:
             print("You are not allowed to delete the movie")

    else:
        return redirect('movie_app:index')
    return redirect("accounts:login")


def add_review(request,id):
    if request.user.is_authenticated:
        movies=Movies.objects.get(id=id)
        if request.method == "POST":
            form=ReviewForm(request.POST or None)
            if form.is_valid():
                data=form.save(commit=False)
                data.comment=request.POST["comment"]
                data.rating=request.POST["rating"]
                data.user=request.user
                data.movies=movies
                data.save()
                return redirect("movie_app:details",id=movies.id)
            else:
                return render(request,'movie_detail.html',{"form":form,"movie":movies})
        else:
            form=ReviewForm()
            return render(request,'add_review.html',{"form":form,"movie":movies})
    else:
        return redirect("accounts:login")