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
    context = {'login_form': AuthenticationForm(), 'signup_form': Register_Form()}
    return render(request, 'home.html', context)


def about(request):
    context = {'login_form': AuthenticationForm(), 'signup_form': Register_Form()}
    return render(request, 'about.html', context)


def cities_index(request):
    if request.method == 'POST':
        city_form = City_Form(request.POST)
        if city_form.is_valid():
            new_city = city_form.save(commit=False)
            new_city.user = request.user
            new_city.save()
            return redirect('cities_index')
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
        'login_form': AuthenticationForm(), 
        'signup_form': Register_Form()
    }
    return render(request, 'profile/detail.html', context)


def cities_detail(request, city_id):
    city = City.objects.get(id=city_id)
    cities = City.objects.all()
    posts = Post.objects.filter(city_id=city.id)
    post_form = Post_Form()
    context = {'login_form': AuthenticationForm(), 'signup_form': UserCreationForm(), 'post_form': post_form, 'city': city ,'posts': posts, 'cities':cities}
    return render(request, 'cities/detail.html', context)




def posts_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    post_form = Post_Form(instance=post)
    context = {
        'post': post,
        'login_form': AuthenticationForm(),
        'signup_form': Register_Form(),
        'post_form': post_form,
    }
    return render(request, 'posts/detail.html' ,context)


# edit post 
def posts_edit(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        post_form = Post_Form(request.POST, instance=post)
        if post_form.is_valid():
            post_form.save()
        return redirect('posts_detail',post_id = post_id)
    else:
        post_form = Post_Form(instance=post)
    context = {'post': post, 'post_form': post_form}
    return render(request, 'cities/detail.html', context)



# delete post
def posts_delete(request, post_id):
    Post.objects.get(id=post_id).delete()
    return redirect("cities_index" )


def new_post(request, city_id):
    # return HttpResponse(city_id)
    if request.method == 'POST':
        post_form = Post_Form(request.POST )
        city = City.objects.get(id=city_id)
        if post_form.is_valid():
            new_form =  post_form.save(commit=False)
            new_form.user = request.user
            new_form.city = city
            new_form.save()
            return redirect('cities_detail', city_id=city_id)
    posts = Post.objects.all()
    post_form = Post_Form()
    context = {'posts':posts, 'post_form': post_form}
    return render(request, 'cities/detail.html', context)




# # Create your views here. 
# def hotel_image_view(request): 
  
#     if request.method == 'POST': 
#         form = HotelForm(request.POST, request.FILES) 
  
#         if form.is_valid(): 
#             form.save() 
#             return redirect('success') 
#     else: 
#         form = HotelForm() 
#     return render(request, 'hotel_image_form.html', {'form' : form}) 
  
  
# def success(request): 
#     return HttpResponse('successfully uploaded') 









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




@login_required
def profile_edit(request, user_id):

    user = User.objects.get(id=user_id)
    
    if request.method == 'POST':
        prof_form = Profile_Form(request.POST ,request.FILES, instance=user.profile)
        user_form = User_Form(request.POST, instance=user)
        if prof_form.is_valid() and user_form.is_valid():
                prof_form.save()
                user_form.save()
                return redirect('profile_detail', user_id=user.id)
    else:
        prof_form = Profile_Form(instance=user.profile)
        user_form = User_Form(instance=user)
    context = {'user':user, 'prof_form':prof_form,'user_form':user_form}
    return render( request, 'profile/edit.html', context)

