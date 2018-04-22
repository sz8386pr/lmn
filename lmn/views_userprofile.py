from django.shortcuts import render
from .models import UserProfile
from django.contrib.auth.models import User

def my_profile(request):
    '''create views for editing user profile'''
    userprofile = User.objects.get()
    return render(request, 'lmn/users/my_profile.html', {'userprofile': userprofile})
