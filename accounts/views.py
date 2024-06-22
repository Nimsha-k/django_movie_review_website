from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.decorators import login_required
from .forms import UserForm, ProfileForm
from django.conf import settings
from movie_app.models import Movies
# Create your views here.
def register(request):
    if request.user.is_authenticated:
        return redirect("movie_app:index")
    else:
        if request.method == "POST":
            form=RegistrationForm(request.POST or None)
            if form.is_valid():
                user=form.save()

                raw_password=form.cleaned_data.get('password1')

                user=authenticate(username=user.username,password=raw_password)
                if user is not None:
                    login(request, user)
                    # Add a welcome message
                    messages.success(request, f"Welcome, {user.username}! Your account has been created successfully.")
                    return redirect("movie_app:index")
                login(request,user)

                return redirect("movie_app:index")
        else:
            form=RegistrationForm()
        return render(request,"register.html",{'form':form})


def login_user(request):
    if request.user.is_authenticated:
        return redirect('movie_app:index')
    else:
        if request.method == "POST":
            username=request.POST['username']
            password=request.POST['password']
            # To check credentials
            user=authenticate(username=username,password=password)
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return redirect("movie_app:index")
                else:
                    return render(request,'login.html',{"error":"your account has been disabled."})
            else:
                return render(request,"login.html",{"error":"Invalid username or  password.Try Again"})
        return render(request,'login.html')



def logout_user(request):
    logout(request)
    return redirect("accounts:login")



@login_required
def profile(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('accounts:profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    movies = Movies.objects.filter(user=request.user)

    return render(request, 'profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'movies': movies
    })
@login_required
def view_profile(request):
    return render(request, 'profile.html', {'user': request.user})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('accounts:view_profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
