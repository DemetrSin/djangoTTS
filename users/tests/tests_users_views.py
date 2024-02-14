from datetime import datetime

from django.test import TestCase, Client
from django.urls import reverse
from users.forms import UserProfileForm, AnonymousHomeTTSForm
from users.models import CustomUser, Subscription


class HomeViewTestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_get(self):
        response = self.client.get(reverse('home'))
        self.assertIsInstance(response.context['form'], AnonymousHomeTTSForm)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/home.html')
        self.assertFalse(response.context['user_info'])

    def test_post_valid(self):
        response = self.client.post(reverse('home'), {'text': 'Some text'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/home.html')
        self.assertIsNotNone(response.context['audio_file_url'])
        self.assertFalse(response.context['fail'])

    def test_post_invalid(self):
        response = self.client.post(reverse('home'), {'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/home.html')
        self.assertTrue(response.context['form'].errors)

    def test_post_unavailable_text_length(self):
        response = self.client.post(reverse('home'), {'text': f'{"a"*501}'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/home.html')
        self.assertTrue(response.context['fail'])


class UserProfileViewTestCase(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username='Nike',
            auth0_id='google12313213',
            email='any@gmail.com',
            password='password',
            is_premium=False
        )
        self.client.force_login(self.user)

    def test_get_with_subscription(self):
        subscription = Subscription.objects.create(user=self.user, end_date=datetime(2000, 12, 28, 12, 12, 12, 12), is_active=True)
        response = self.client.get(reverse('profile', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')
        self.assertEqual(response.context['subscription'], subscription)
        self.assertTrue(response.context['user_profile'])

    def test_get_without_subscription(self):
        response = self.client.get(reverse('profile', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')
        self.assertIsNone(response.context['subscription'])
        self.assertTrue(response.context['user_profile'])
