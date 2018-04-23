from django.test import TestCase

from django.contrib.auth.models import User
from django.db import IntegrityError
from lmn.forms import UserRegistrationForm
# Create your tests here.


class TestUser(TestCase):

    def test_create_user_all_fields_required(self):
        #fails
        # TODO is this testing the right thing?

        u = {'username': '',
             'first_name': '',
             'last_name': '',
             'email': '',
             'password1': '',
             'password2': ''}
        form = UserRegistrationForm(u)
        with self.assertRaises(ValueError):
            form.save()

        u = {'username':'bob'}
        form = UserRegistrationForm(u)
        with self.assertRaises(ValueError):
            form.save()

        u = {'username': 'bob',
             'first_name': '',
             'last_name': '',
             'email': 'bob@bob.com',
             'password1': '',
             'password2': ''}
        form = UserRegistrationForm(u)
        with self.assertRaises(ValueError):
            form.save()

        u = {'username': 'bob',
             'first_name': 'bob',
             'last_name': '',
             'email': 'bob@bob.com',
             'password1': '',
             'password2': ''}
        form = UserRegistrationForm(u)
        with self.assertRaises(ValueError):
            form.save()


    def test_create_user_duplicate_username_fails(self):
        #fails
        user = {'username': 'steve',
             'first_name': 'bob',
             'last_name': 'bob',
             'email': 'bob@bob.com',
             'password1': '1234',
             'password2': '1234'}
        form = UserRegistrationForm(user)
        form.save()

        user2 = {'username': 'steve',
             'first_name': 'bob',
             'last_name': 'bob',
             'email': 'another_bob@bob.com',
             'password1': '1234',
             'password2': '1234'}
        form2 = UserRegistrationForm(user2)
        with self.assertRaises(ValueError):
            form2.save()


    def test_create_user_duplicate_username_case_insensitive_fails(self):
        #fails
        user = User(username='bob', email='bob@bob.com', first_name='bob', last_name='bob')
        UserRegistrationForm(user)

        user2 = User(username='Bob', email='another_bob@bob.com', first_name='bob', last_name='bob')
        with self.assertRaises(IntegrityError):
            UserRegistrationForm(user2)


    def test_create_user_duplicate_email_fails(self):
        user = User(username='bob', email='bob@bob.com', first_name='bob', last_name='bob')
        UserRegistrationForm(user)

        user2 = User(username='bob', email='bob@bob.com', first_name='bob', last_name='bob')
        with self.assertRaises(IntegrityError):
            UserRegistrationForm(user2)


    def test_create_user_duplicate_email_case_insensitive_fails(self):
        user = User(username='bob', email='bob@bob.com', first_name='bob', last_name='bob')
        user.save()

        user2 = User(username='another_bob', email='Bob@bob.com', first_name='bob', last_name='bob')
        with self.assertRaises(IntegrityError):
            user2.save()
