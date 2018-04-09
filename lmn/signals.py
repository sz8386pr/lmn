from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from lmn.models import Note
import logging
from django.core.files.storage import default_storage

# Cleanup(delete) Note object from python.
@receiver(post_delete, sender=Note)
def note_delete_image_cleanup(sender, **kwargs):
    note = kwargs['instance']
    if notes.object.photo:
        logging.info(notes.object.photo)
        if default_storage.exists(notes.object.photo.name):
            default_storage.delete(notes.object.photo.name)


@receiver(pre_save, sender=Note)
def notes_pre_save_image_cleanup(sender, **kwarg):
    new_note = kwargs['instance']

    # Get pk and query db for prevoius values.
    old_note = Note.objects.filter(pk=new_note.filter).first()

    # If there is a photo, delete it.
    if old_note and old_note.photo:
        if default_storage.exists(old_note.photo.name):
            logging.info('delete', old_note.photo.name)
            default_storage.delete(old_note.photo.name)
