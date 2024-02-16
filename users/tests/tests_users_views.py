import os
from datetime import datetime

from django.conf import settings
from django.test import Client, TestCase
from django.urls import reverse

from users.forms import AnonymousHomeTTSForm, UserProfileForm
from users.models import CustomUser, Subscription
from users.views import UserProfileView


class HomeViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get(self):
        response = self.client.get(reverse('home'))
        self.assertIsInstance(response.context['form'], AnonymousHomeTTSForm)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/home.html')
        self.assertFalse(response.context['user_info'])

    def test_post_valid(self):
        response = self.client.post(reverse('home'), {'text': 'some text'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/home.html')
        self.assertIsNotNone(response.context['audio_file_url'])
        self.assertFalse(response.context['fail'])
        self.assertTrue(response.context['form'].is_valid())
        os.remove(os.path.join(settings.MEDIA_ROOT, 'some.mp3'))

    def test_post_invalid(self):
        response = self.client.post(reverse('home'), {'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/home.html')
        self.assertTrue(response.context['form'].errors)

    def test_post_unavailable_text_length(self):
        response = self.client.post(reverse('home'), {'text': f'{"a" * 501}'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/home.html')
        self.assertTrue(response.context['fail'])


class UserProfileViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.view = UserProfileView()
        self.user = CustomUser.objects.create_user(
            username='Nike',
            auth0_id='google12313213',
            email='any@gmail.com',
            password='password',
            is_premium=False
        )
        self.client.force_login(self.user)

    def test_get_with_subscription(self):
        subscription = Subscription.objects.create(
            user=self.user,
            end_date=datetime(2000, 12, 28, 12, 12, 12, 12),
            is_active=True
        )
        response = self.client.get(reverse('profile', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')
        self.assertEqual(response.context['subscription'], subscription)
        self.assertTrue(response.context['user_profile'])
        self.assertEqual(self.view.model, CustomUser)
        self.assertEqual(self.view.form_class, UserProfileForm)
        self.assertEqual((response.context['user_profile'].username,
                          response.context['user_profile'].email,
                          response.context['user_profile'].auth0_id,
                          response.context['user_profile'].is_premium,
                          ),
                         ('Nike',
                          'any@gmail.com',
                          'google12313213',
                          False
                          ))

    def test_get_without_subscription(self):
        response = self.client.get(reverse('profile', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')
        self.assertIsNone(response.context['subscription'])
        self.assertTrue(response.context['user_profile'])
        self.assertEqual(self.view.model, CustomUser)
        self.assertEqual(self.view.form_class, UserProfileForm)

    def test_unauthenticated_access(self):
        self.client.logout()
        response = self.client.get(reverse('profile', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)


class EditProfileViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username='Nike',
            auth0_id='google12313213',
            email='any@gmail.com',
            password='password',
            is_premium=False
        )
        self.client.force_login(self.user)

    def test_get(self):
        response = self.client.get(reverse('edit_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('users/edit_profile.html')
        self.assertIsInstance(response.context['form'], UserProfileForm)

    def test_valid_post(self):
        response = self.client.post(reverse('edit_profile'), {'username': 'Adik'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('profile', kwargs={'pk': self.user.pk}))
        self.assertTemplateUsed('users/edit_profile.html')
        self.assertEqual(CustomUser.objects.get(pk=self.user.pk).username, 'Adik')

    def test_invalid_post(self):
        response = self.client.post(reverse('edit_profile'), {})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertFormError(response, 'form', 'username', "This field is required.")

    def test_unauthenticated_access(self):
        self.client.logout()
        response = self.client.get(reverse('edit_profile'))
        self.assertEqual(response.status_code, 302)


class SubscriptionViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username='Nike',
            auth0_id='google12313213',
            email='any@gmail.com',
            password='password',
            is_premium=False
        )
        self.client.force_login(self.user)

    def test_get(self):
        response = self.client.get(reverse('subscription'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('users/subscription.html')

    def test_unauthorised_access(self):
        self.client.logout()
        response = self.client.get(reverse('subscription'))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed('users/subscription.html')

    def test_valid_post(self):
        response = self.client.post(reverse('subscription'), {'duration': 30})
        self.assertTemplateNotUsed('users/subscription.html')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('profile', kwargs={'pk': self.user.pk}))
        self.assertTrue(Subscription.objects.filter(user=self.user, is_active=True).exists())
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_premium)

    def test_invalid_post(self):
        with self.assertRaises(TypeError):
            self.client.post(reverse('subscription'), {})
