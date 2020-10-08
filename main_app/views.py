from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import City, Post, Profile
from .forms import City_Form, Post_Form, Profile_Form, User_Form
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    context = {'login_form': AuthenticationForm(), 'signup_form': UserCreationForm()}
    return render(request, 'home.html', context)


def about(request):
    context = {'login_form': AuthenticationForm(), 'signup_form': UserCreationForm()}
    return render(request, 'about.html', context)


def cities_index(request):
    # if request.method == 'POST':
    #     city_form = City_Form(request.POST)
    #     if city_form.is_valid():
    #         new_city = city_form.save(commit=False)
    #         new_city.user = request.user
    #         new_city.save()
    #         return redirect('cities_index')
    # cities = City.objects.filter(user=request.user)
    # city_form = City_Form()
    # context = {'cities':cities, 'city_form': city_form, 'login_form': AuthenticationForm(), 'signup_form': UserCreationForm()}
    return render(request, 'cities/index.html')
    # return render(request, 'cities/index.html', context)





# def user_detail(request, user_id):
#     user = User.objects.get(id=user_id)
#     context = {'user': user}
#     return render(request, 'profile/detail.html', context)

def profile_detail(request):
    user = request.user
    context = {'user': user}
    return render(request, 'profile/detail.html', context)




def cities_detail(request):
    context = {'login_form': AuthenticationForm(), 'signup_form': UserCreationForm()}
    return render(request, 'cities/detail.html', context)

# --- This functionality will by admin-only and accessible through the admin page, so we shouldn't need view functions to handle them ---
# def cities_delete(request):
#     return HttpResponse( '<h1>cities_delete</h1>')
# def cities_edit(request):
#     return HttpResponse( '<h1>cities_edit</h1>')

    
# def signup(request):
#     # return HttpResponse( '<h1>signup</h1>')
#     error_message = ''
#     if request.method == 'POST':
#     # This is how to create a 'user' form object
#     # that includes the data from the browser
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             # This will add the user to the database
#             user = form.save()
#             # This is how we log a user in via code
#             login(request, user)
#             return redirect('cats_index')
#         else:
#             error_message = 'Invalid sign up - try again'
#     # A GET or a bad POST request, so render signup.html with an empty form
#     form = UserCreationForm()
#     context = {'form': form, 'error_message': error_message}
#     return render(request, 'registration/signup.html', context)




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
