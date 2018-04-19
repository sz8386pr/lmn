from django.shortcuts import render, redirect, get_object_or_404

from .models import Venue, Artist, Note, Show
from .forms import VenueSearchForm, NewNoteForm, ArtistSearchForm, UserRegistrationForm, UserEditForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http.response import HttpResponseForbidden
from tzlocal import get_localzone
from django.utils.timezone import activate

activate(get_localzone())

from django.utils import timezone



def user_profile(request, user_pk):
    activate(get_localzone())
    users_profile = User.objects.get(pk=user_pk)
    user = request.user
    usernotes = Note.objects.filter(user=users_profile.pk).order_by('posted_date').reverse()

    return render(request, 'lmn/users/user_profile.html', {'user' : user, 'users_profile' : users_profile, 'notes' : usernotes })



@login_required
def my_user_profile(request):
    # TODO - editable version for logged-in user to edit own profile
    return redirect('lmn:user_profile', user_pk=request.user.pk)



def register(request):

    if request.method == 'POST':

        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(username=request.POST['username'], password=request.POST['password1'])
            login(request, user)
            return redirect('lmn:homepage')

        else :
            message = 'Please check the data you entered'
            return render(request, 'registration/register.html', { 'form' : form , 'message' : message } )


    else:
        form = UserRegistrationForm()
        return render(request, 'registration/register.html', { 'form' : form } )


@login_required
def edit_user(request, user_pk):

    user = get_object_or_404(User, pk=user_pk)
    form = UserEditForm(instance=user)

    # if invalid user somehow gets this page
    if request.user != user:

        #Can alter to redirect or render a template to be added
        return HttpResponseForbidden("ERROR: You may only alter your profile.")

    # otherwise continue...
    if request.method == 'POST':

        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('lmn:user_profile', user_pk=user_pk)

        else:
            message = 'Please check the data you entered'
            return render(request, ('lmn/users/edit_user.html', user_pk), {'form': form, 'message': message})

    else:
        return render(request, ('lmn/users/edit_user.html', user_pk), {'form': form, 'user': user})
