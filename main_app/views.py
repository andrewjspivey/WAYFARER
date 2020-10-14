from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import City, Post, Profile, Comment
from .forms import City_Form, Post_Form, Profile_Form, User_Form, Register_Form , Comment_Form
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.core import mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.template.loader import render_to_string



# Form constants
register_form = Register_Form()
login_form = AuthenticationForm()
comment_form = Comment_Form()


# Create your views here.

# HOME PAGE WITH CAROUSEL OF CITIES & APP INFO
def home(request):
    cities = City.objects.all()
    context = {'login_form': login_form, 'signup_form': register_form, 'cities': cities}
    return render(request, 'home.html', context)


# DEVELOPER DETAILS ON APP CREATORS OF WAYFARER
def about(request):
    context = {'login_form': login_form, 'signup_form': register_form}
    return render(request, 'about.html', context)


# CITIES INDEX PAGE (NO LONGER REQUIRED)
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
    context = {'cities':cities, 'city_form': city_form, 'login_form': login_form, 'signup_form': register_form}
    return render(request, 'cities/index.html', context)



# CITIES INDEX PAGE WITH CITY DETAIL, AT CITY DETAIL PAGE
def cities_detail(request, city_id):
    city = City.objects.get(id=city_id)
    cities = City.objects.all()
    posts = Post.objects.filter(city_id=city.id)
    post_form = Post_Form()
    page = request.GET.get('page', 1)
    paginator = Paginator(posts, 3)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    
    context = {
        'login_form': login_form, 
        'signup_form': register_form, 
        'post_form': post_form, 
        'city': city,
        'posts': posts, 
        'cities':cities
    }
    return render(request, 'cities/detail.html', context)



# POST DETAIL PAGE INCLUDES:
def posts_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    post_form = Post_Form(instance=post)
    comments = Comment.objects.filter(post_id=post.id)
    page = request.GET.get('page', 1)
    paginator = Paginator(comments, 5)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        commnts = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    context = {
        'post': post,
        'login_form': login_form,
        'signup_form': register_form,
        'post_form': post_form,
        'comment_form': comment_form,
        'comments': comments
    }
    return render(request, 'posts/detail.html', context)


# CREATE NEW POST WHILE ON CITY PAGE
@login_required
def new_post(request, city_id):
    if request.method == 'POST':
        post_form = Post_Form(request.POST, request.FILES)
        city = City.objects.get(id=city_id)
        if post_form.is_valid():
            new_form =  post_form.save(commit=False)
            new_form.user = request.user
            new_form.city = city
            new_form.save()
            return redirect('cities_detail', city_id=city_id)
    posts = Post.objects.all()
    post_form = Post_Form()
    context = {
        'posts':posts, 
        'post_form': post_form
        }
    return render(request, 'cities/detail.html', context)


# EDIT POST AT POST DETAIL PAGE 
@login_required
def posts_edit(request, post_id):

    post = Post.objects.get(id=post_id)
    if request.method == 'POST' and request.user == post.user:
        post_form = Post_Form(request.POST, instance=post)
        if post_form.is_valid():
            post_form.save()
        return redirect('posts_detail',post_id = post_id)
    else:
        post_form = Post_Form(instance=post)
    context = {'post': post, 'post_form': post_form}
    return render(request, 'cities/detail.html', context)


# DELETE POST AT POST DETAIL PAGE
@login_required
def posts_delete(request, post_id):
    Post.objects.get(id=post_id).delete()
    return redirect("cities_index" )



# adds comment on post
def add_comments(request, post_id):
    post = Post.objects.get(id = post_id)
    if request.method == 'POST':
        comment_form = Comment_Form(request.POST)
        if comment_form.is_valid():
            new_form =  comment_form.save(commit=False)
            new_form.post = post
            new_form.user = request.user
            new_form.save()
            return redirect('posts_detail', post_id=post_id)
    comments = Comment.objects.all()
    comment_form = Comment_Form()
    context = {
        'post': post,
        'comments':comments, 
        'comment_form': comment_form
        }
    return render(request, 'posts/detail.html', context)


# DELETE COMMENT 

def comments_delete(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    post = Post.objects.get(id=comment.post.id)
    comment.delete()
    return redirect('posts_detail', post_id=post.id)



# PROFILE DETAIL PAGE INCLUDES
@login_required
def profile_detail(request, slug):
    profile = Profile.objects.get(slug=slug)
    user = User.objects.get(id=profile.user.id)
    profile_form = Profile_Form(user.profile)
    user_form = User_Form(user)
    posts = Post.objects.filter(user_id=user.id)
    
    all_posts = Post.objects.all()
    city_count = {}

    for post in all_posts:
        if post.city in city_count:
            city_count[post.city] += 1
        else:
            city_count[post.city]= 1

    city_count = {key:value for key, value in city_count.items() if value >0}
    print(city_count)


    page = request.GET.get('page', 1)
    paginator = Paginator(posts, 3)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'city_count':city_count,
        'slug':user.profile.slug,
        'profile':profile,
        'user': user,
        'posts': posts,
        'prof_form': Profile_Form(instance=user.profile),
        'user_form': User_Form(instance=user),
        'login_form': login_form, 
        'signup_form': register_form
    }
    return render(request, 'profile/detail.html', context)


# SIGN UP IN MODAL AT ANY PAGE WITHIN THE APP
def signup(request):
    if request.method == 'POST':
        error_message = 'Invalid signup. Try again.'
        form = Register_Form(request.POST)
        print('TAKE A CLOSER LOOK AT THAT FORM')
        print(form)
        if form.is_valid():
            print('Form is valid')
            user = form.save()
            city_id = City.objects.get(id=request.POST['current_city'])
            profile = Profile.objects.create(
                user = user,
                current_city = city_id
            )
            profile.save()
            with mail.get_connection() as connection:
                user = User.objects.get(id=user.id)
                mail.EmailMessage(
                    'Welcome to Wayfarer',
                    'Wayfarer is so excited to have you in our community of city trackers experience makers! Stay up do date by regularly logging-in to Wayfarer.com',
                    'wayfarer_team@wayfarer.com',
                    [user.email],
                    connection=connection
                ).send()
            login(request, user)
            return redirect('profile_detail', slug=user.profile.slug)
    
        context = {
            # 'slug':user.profile.slug,
            'slug':user.username,
            'error_message': error_message,
            'signup_form': register_form,
            'login_form': login_form
        }
        return render(request, 'registration/signup.html', context)


# LOGIN IN MODAL AT ANY PAGE IN APP
def custom_login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('profile_detail', slug=user.profile.slug)
    else:
        context = {
            'slug':user.id,
            'error_message': 'Invalid Login. Try again.',
            'login_form': login_form,
            'signup_form': register_form
        }
        return render(request, 'registration/login.html', context)

# 'slug':user.profile.slug,
# 'slug':user.profile.slug,
# 'slug':user.profile.slug,

# EDIT PROFILE DETAILS (EXCEPT PASSWORD & USERNAME) AT PROFILE DETAIL PAGE
@login_required
def profile_edit(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        if user != request.user:
            return redirect('/')
        prof_form = Profile_Form(request.POST, request.FILES, instance=user.profile)
        user_form = User_Form(request.POST, instance=user)
        if prof_form.is_valid() and user_form.is_valid():
            prof_form.save()
            user_form.save()
            return redirect('profile_detail', slug=user.profile.slug)
    else:
        prof_form = Profile_Form(instance=user.profile)
        user_form = User_Form(instance=user)
    context = {'user':user, 'prof_form':prof_form,'user_form':user_form}
    return render( request, 'profile/edit.html', context)

