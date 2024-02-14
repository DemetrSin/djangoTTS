from django.test import TestCase
from users.forms import UserProfileForm, AnonymousHomeTTSForm
from users.models import CustomUser, AnonymousFiles


class UserProfileFormTestCase(TestCase):

    def test_valid_data(self):
        form = UserProfileForm(
            {
                'username': 'test'
            }
        )
        self.assertTrue(form.is_valid())

    def test_invalid_data(self):
        form = UserProfileForm(
            {
                'username': ''
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

    def test_meta_fields(self):
        form = UserProfileForm
        self.assertEqual(form.Meta.model, CustomUser)
        self.assertEqual(form.Meta.fields, ['username'])


class AnonymousHomeTTSFormTestCase(TestCase):

    def test_valid_form(self):
        form = AnonymousHomeTTSForm(
            {
                'text': 'Some text'
            }
        )
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = AnonymousHomeTTSForm(
            {
                'text': ''
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

    def test_meta_field(self):
        form = AnonymousHomeTTSForm()
        self.assertEqual(form.Meta.model, AnonymousFiles)
        self.assertEqual(form.Meta.fields, ['text'])

