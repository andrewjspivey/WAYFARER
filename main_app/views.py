from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import City,Post
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def cities_index(request):
    # return HttpResponse( '<h1>cities_index</h1>')
    if request.method == 'POST':
        city_form = City_Form(request.POST)
        if city_form.is_valid():
            new_city = city_form.save(commit=False)
            new_city.user = request.user
            new_user.save()
            return redirect('cities_index')
    cities = City.objects.filter(user=request.user)
    city_form = City_Form()
    context = {' cities':cities, 'city_form': city_form}
    return render(request, 'profile/detail.html', context)





def user_detail(request, user_id):
    # return render(request, 'profile/detail.html')
    user = User.objects.get(id=user_id)
    context = {'user': user}
    return render(request, 'profile/detail.html', context)


def cities_index(request):
    return render(request, 'cities/index.html')



def cities_detail(request):
    return render(request, 'cities/detail.html')

# --- This functionality will by admin-only and accessible through the admin page, so we shouldn't need view functions to handle them ---
# def cities_delete(request):
#     return HttpResponse( '<h1>cities_delete</h1>')
# def cities_edit(request):
#     return HttpResponse( '<h1>cities_edit</h1>')

    
def signup(request):
    return HttpResponse( '<h1>signup</h1>')






