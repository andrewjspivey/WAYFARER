from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import City, Post, Profile
from .forms import City_Form, Post_Form, Profile_Form, User_Form, Register_Form
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.core import mail
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.template.loader import render_to_string



# Form constants
register_form = Register_Form()
login_form = AuthenticationForm()

# Create your views here.

# HOME PAGE WITH CAROUSEL OF CITIES & APP INFO
def home(request):
    context = {'login_form': login_form, 'signup_form': register_form}
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


# PROFILE DETAIL PAGE
def profile_detail(request, user_id):
    user = User.objects.get(id=user_id)
    profile_form = Profile_Form(instance=user.profile)
    user_form = User_Form(instance=user)
    context = {
        'user': user,
        'profile_form' : profile_form,
        'user_form' : user_form,
        'login_form': login_form, 
        'signup_form': register_form
    }
    return render(request, 'profile/detail.html', context)


# # PROFILE DETAIL PAGE
# def profile_detail(request, slug):
#     user = User.objects.get(slug=slug)
#     profile_form = Profile_Form(instance=slug.profile)
#     user_form = User_Form(instance=slug)
#     context = {
#         'slug': user,
#         'profile_form' : profile_form,
#         'user_form' : user_form,
#         'login_form': login_form, 
#         'signup_form': register_form
#     }
#     return render(request, 'profile/detail.html', context)


# CITIES INDEX PAGE WITH CITY DETAIL, AT CITY DETAIL PAGE
def cities_detail(request, city_id):
    city = City.objects.get(id=city_id)
    cities = City.objects.all()
    posts = Post.objects.filter(city_id=city.id)
    post_form = Post_Form()
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
    context = {
        'post': post,
        'login_form': login_form,
        'signup_form': register_form,
        'post_form': post_form,
    }
    return render(request, 'posts/detail.html' ,context)


# CREATE NEW POST WHILE ON CITY PAGE
@login_required
def new_post(request, city_id):
    if request.method == 'POST':
        post_form = Post_Form(request.POST)
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
    if request.method == 'POST':
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


# PROFILE DETAIL PAGE INCLUDES
def profile_detail(request, user_id):
    user = User.objects.get(id=user_id)
    profile_form = Profile_Form()
    user_form = User_Form()
    context = {
        'user': user,
        'profile_form' : profile_form,
        'user_form' : user_form,
        'login_form': login_form, 
        'signup_form': register_form
    }
    return render(request, 'profile/detail.html', context)
# # PROFILE DETAIL PAGE INCLUDES
# def profile_detail(request, slug):
#     user = User.objects.get(slug=slug)
#     profile_form = Profile_Form()
#     user_form = User_Form()
#     context = {
#         'user': user,
#         'profile_form' : profile_form,
#         'user_form' : user_form,
#         'login_form': login_form, 
#         'signup_form': register_form
#     }
#     return render(request, 'profile/detail.html', context)



# SIGN UP IN MODAL AT ANY PAGE WITHIN THE APP
def signup(request):
    if request.method == 'POST':
        error_message = 'Invalid signup. Try again.'
        form = Register_Form(request.POST)
        if form.is_valid():
            user = form.save()
            city_id = City.objects.get(id=request.POST['current_city'])
            profile = Profile.objects.create(
                user = user,
                current_city = city_id
            )
            profile.save()
            with mail.get_connection() as connection:
                # user = User.objects.get(id=user.id)
                mail.EmailMessage(
                    'Welcome to Wayfarer',
                    'Wayfarer is so excited to have you in our community of city trackers experience makers! Stay up do date by regularly logging-in to Wayfarer.com',
                    'wayfarer_team@wayfarer.com',
                    [user.email],
                    connection=connection
                ).send()
            login(request, user)
            
            # mail.EmailMessage(
            #     subject2, body2, from2, [user.email],
            #     connection=connection
            # ).send()
            
            # send_mail(
            #     'Welcome to Wayfarer',
            #     'Wayfarer is so excited to have you in our community of city trackers experience makers! Stay up do date by regularly logging in to Wayfarer.com',
            #     'wayfarer_team@hushmail.com',
            #     [user.profile.email],
            #     fail_silently=False,
            # )
            # print(f'{user.profile.username} has been sent an email at {user.profile.email}')
            # return render(request, 'send/index.html')

            return redirect('profile_detail', user_id=user.id)
    
        context = {
            'error_message': error_message,
            'signup_form': register_form,
            'login_form': login_form
        }
        return render(request, 'registration/signup.html', context)


        


        # def send_email(request):




        #     # print('SIGNUP Function POST IS FORM VALID?????')

        #     formsave = form.save(commit=False)
            
        #     firstname = form.cleaned_data.get("first_name")
        #     lastname = form.cleaned_data.get("last_name")
        #     emailvalue = form.cleaned_data.get("email")
        #     uservalue = form.cleaned_data.get("username")
        #     passwordvalue1 = form.cleaned_data.get("password1")
        #     passwordvalue2 = form.cleaned_data.get("password2")

        #     if passwordvalue1 == passwordvalue2:
        #         try:
        #             user = User.objects.get(username = uservalue)
        #             context = {'form':form, 'error_message':'The username you entered already exists. Try again.'}
        #             # email = User.objects.get(email = emailvalue)
        #             return render(request, 'registration/signup.html', context)
        #         except User.DoesNotExist:
        #             # user = User.objects.create_user(uservalue, password = passwordvalue1, email=emailvalue)

        #             # This will add the user to the database
        #             user = formsave.save()
        #             city_id = City.objects.get(id=request.POST['current_city'])
        #             profile = Profile.objects.create(
        #                 user = user,
        #                 current_city = city_id
        #             )
        #             profile.save()

        #             # This is how we log a user in via code
        #             login(request, user)
                    
        #             # formsave.user = request.user

        #             # formsave.save()

        #             context = {'form':form, 'user_id':user.id}
        #             # print('line225')
        #             # return render(request, 'registration/signup.html', context)               
                    
        #             return redirect('profile_detail', context)

        #     else:
        #         context = {'form':form, 'error_message': 'The passwords that you provided don\'t match'}
        #         print('line233')
        #         return render(request, 'registration/signup.html', context)               

        #             # error_message = 'Invalid sign up - try again'
        #     # A GET or a bad POST request, so render signup.html with an empty form
        # else: 
        #     # print('BEFORE USERCREATION FORM UNDER THE LAST ELSE STATEMENT')

        #     form = UserCreationForm()
        #     context = {'form': form, 'error_message': error_message}
        #     # print('line241')
        #     # return render(request, 'home.html', context)
        #     return render(request, 'registration/signup.html', context)
    






# def success(request, uid):
#     template = render_to_string('send/email_template.html', {'name': request.user.profile.first_name})


#     email = EmailMessage(
#         'Welcome to Wayfarrer',
#         template,
#         settings.EMAIL_HOST_USER,
#         [request.user.profile.email]
#     )
#     email.fail_silently=False
#     email.send()

#     wayfarer_project = wayfarer_project.objects.get(id=uid)
#     context = {'wayfarer_project':wayfarer_project}
    
#     return render(request, 'send')


# def contact(request):
#     if request.method == "POST":
#         message_name = request.POST['message_name']
#         message_email = request.POST['message_email']
#         message = request.POST['message']


#         # send an email
#         send_mail(

#             message_name, # subject
#             message, # message
#             message_email, # from email
#             ['wayfareruser@swanticket.com'], # to email
#         )

#         return render(request, 'contact.html', {'message_name':message)name})
#     else:
#         return render(request, 'contact.html', {})





# LOGIN IN MODAL AT ANY PAGE IN APP
def custom_login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('profile_detail', user_id=user.id)
    else:
        context = {
            'error_message': 'Invalid Login. Try again.',
            'login_form': login_form,
            'signup_form': register_form
        }
        return render(request, 'registration/login.html', context)


# EDIT PROFILE DETAILS (EXCEPT PASSWORD & USERNAME) AT PROFILE DETAIL PAGE
@login_required
def profile_edit(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        prof_form = Profile_Form(request.POST, instance=user.profile)
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

