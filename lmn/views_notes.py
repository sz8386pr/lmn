from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404

from .models import Venue, Artist, Note, Show
from .forms import VenueSearchForm, NewNoteForm, EditNoteForm, ArtistSearchForm, UserRegistrationForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http.response import HttpResponseForbidden

from django.contrib import messages
from . import photo_manager
import copy

from django.utils import timezone


@login_required
def new_note(request, show_pk):

    show = get_object_or_404(Show, pk=show_pk)

    if request.method == 'POST' :

        form = NewNoteForm(request.POST, request.FILES)
        if form.is_valid():

            note = form.save(commit=False)
            if note.title and note.text:  # If note has both title and text
                note.user = request.user
                note.show = show
                note.posted_date = timezone.now()
                note.save()
                return redirect('lmn:note_detail', note_pk=note.pk)

    else :
        form = NewNoteForm()

    return render(request, 'lmn/notes/new_note.html' , {'form': form , 'show':show})



def latest_notes(request):
    notes = Note.objects.all().order_by('posted_date').reverse()

    paginator = Paginator(notes, 5)

    page = request.GET.get('page')
    notes = paginator.get_page(page)

    return render(request, 'lmn/notes/note_list.html', {'notes':notes})


def notes_for_show(request, show_pk):   # pk = show pk

    # Notes for show, most recent first
    notes = Note.objects.filter(show=show_pk).order_by('posted_date').reverse()
    show = Show.objects.get(pk=show_pk)  # Contains artist, venue

    paginator = Paginator(notes, 5)

    page = request.GET.get('page')
    notes = paginator.get_page(page)

    return render(request, 'lmn/notes/note_list.html', {'show':show, 'notes':notes})


@login_required
def note_details(request, note_pk):

    note = get_object_or_404(Note, pk=note_pk)

    twitterArtist = ''.join(note.show.artist.name.split())
    twitterVenue = ''.join(note.show.venue.name.split())
    twitterCity = ''.join(note.show.venue.city.split() + note.show.venue.state.split())

    if request.user != note.user:

        #Can alter to redirect or render a template to be added
        return HttpResponseForbidden("ERROR: You may only alter your own notes.")

    else:

        if request.method == 'POST':


            old_note = get_object_or_404(Note, pk=note_pk)

            form = EditNoteForm(request.POST, request.FILES, instance=note)
            if form.is_valid():


                # Delete any old photo
                if 'photo' in form.changed_data:
                    photo_manager.delete_photo(old_note.photo)

                form.save()

                messages.info(request, 'Note information updated!')

            else:
                messages.error(request, form.errors)

            return redirect('lmn:note_detail', note_pk=note_pk)


        else:

            if note.posted_date:
                edit_form = EditNoteForm(instance=note)
                return render(request, 'lmn/notes/note_detail.html', { 'note' : note, 'edit_form' : edit_form, 'twitterArtist' : twitterArtist,
                                                                       'twitterVenue' : twitterVenue, 'twitterCity': twitterCity} } )

            else:

                return render(request, 'lmn/notes/note_detail.html' , { 'note' : note, 'twitterArtist' : twitterArtist,
                                                                       'twitterVenue' : twitterVenue, 'twitterCity': twitterCity} })



@login_required
def delete_note(request):

    pk = request.POST['note_pk']
    note = get_object_or_404(Note, pk=pk)

    if request.user != note.user:

        #Can alter to redirect or render a template to be added.
        return HttpResponseForbidden("ERROR: You may only delete your own notes.")

    else:
        note.delete()
        return redirect('lmn:latest_notes')
