from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import City, Post, Profile
from .forms import City_Form, Post_Form, Profile_Form, User_Form, Register_Form
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    # sign up form should be profile form, not just base django user creation form
    context = {'login_form': AuthenticationForm(), 'signup_form': Register_Form()}
    return render(request, 'home.html', context)


def about(request):
    context = {'login_form': AuthenticationForm(), 'signup_form': Register_Form()}
    return render(request, 'about.html', context)


def cities_index(request):
    # profile = Profile.objects.get(id=request.user.id)
    if request.method == 'POST':
        city_form = City_Form(request.POST)
        if city_form.is_valid():
            new_city = city_form.save(commit=False)
            new_city.user = request.user
            new_city.save()
            return redirect('cities_index')
    # cities = City.objects.filter(user=request.user)
    cities = City.objects.all()
    city_form = City_Form()
    context = {'cities':cities, 'city_form': city_form, 'login_form': AuthenticationForm(), 'signup_form': UserCreationForm()}
    return render(request, 'cities/index.html', context)



def profile_detail(request, user_id):
    user = User.objects.get(id=user_id)

    profile_form = Profile_Form()
    user_form = User_Form()
    context = {
        'user': user,
        'profile_form' : profile_form,
        'user_form' : user_form,
    }
    return render(request, 'profile/detail.html', context)


def cities_detail(request, city_id):
    city = City.objects.get(id=city_id)
    posts  = Post.objects.all()
    context = {'login_form': AuthenticationForm(), 'signup_form': UserCreationForm(), 'city': city ,'posts': posts}
    return render(request, 'cities/detail.html', context)

# --- This functionality will by admin-only and accessible through the admin page, so we shouldn't need view functions to handle them ---
# def cities_delete(request):
#     return HttpResponse( '<h1>cities_delete</h1>')
# def cities_edit(request):
#     return HttpResponse( '<h1>cities_edit</h1>')

    
def signup(request):
    error_message = ''
    if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
        # form = UserCreationForm(request.POST)
        form = Register_Form(request.POST)
        if form.is_valid():
            # This will add the user to the database
            user = form.save()
            city_id = City.objects.get(id=request.POST['current_city'])
            profile = Profile.objects.create(
                user = user,
                current_city = city_id
            )
            profile.save()
            # This is how we log a user in via code
            login(request, user)
            return redirect('profile_detail', user_id=user.id)
        else:
            error_message = 'Invalid sign up - try again'
    # A GET or a bad POST request, so render signup.html with an empty form
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)


def custom_login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('profile_detail', user_id=user.id)
    else:
        # TODO figure out frontend error handling?
        return redirect('/accounts/login')


   # EDIT ROUTE
# @login_required
def profile_edit(request, user_id):
    # return HTTPResponse('<h1>PROFILE EDIT is ⇪ and 🏃🏻‍♀️</h1>')
    
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        # prof_form = Profile_Form(request.POST, instance=user)
        # user_form = User_Form(request.POST, instance=user)
        reg_form = Register_Form(request.POST, instance=user)
        # if reg_form.is_valid():
        if reg_form.is_valid():
            reg_form.save()
            # reg_form.save()
            # reg_form.save()
            return redirect('profile_detail', user_id=user.id)
    else:
        reg_form = Register_Form(instance=user)
    context = {'user':user, 'reg_form':reg_form}
    return render( request, 'profile/edit.html', context)
