from django.test import TestCase
from django.urls import reverse, resolve
from users import views
from users.models import CustomUser


class TestUrls(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(username='Nick')

    def test_login_url_resolves(self):
        self.assertEqual(resolve(reverse('login')).func, views.login)
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 302)

    def test_callback_url_resolves(self):
        self.assertEqual(resolve(reverse('callback')).func, views.callback)

    def test_logout_url_resolves(self):
        self.assertEqual(resolve(reverse('logout')).func, views.logout)
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)

    def test_home_url_resolves(self):
        self.client.force_login(self.user)
        self.assertEqual(resolve(reverse('home')).func.view_class, views.HomeView)
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_home_url_unauthorised(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_profile_url_resolves(self):
        self.client.force_login(self.user)
        self.assertEqual(resolve(reverse('profile', args=[1])).func.view_class, views.UserProfileView)
        response = self.client.get(reverse('profile', args=[1]))
        self.assertEqual(response.status_code, 200)

    def test_profile_url_unauthorised(self):
        response = self.client.get(reverse('profile', args=[1]))
        self.assertEqual(response.status_code, 302)

    def test_profile_edit_url_resolves(self):
        self.client.force_login(self.user)
        self.assertEqual(resolve(reverse('edit_profile')).func.view_class, views.EditProfileView)
        response = self.client.get(reverse('edit_profile'))
        self.assertEqual(response.status_code, 200)

    def test_profile_edit_unauthorised(self):
        response = self.client.get(reverse('edit_profile'))
        self.assertEqual(response.status_code, 302)

    def test_subscription_url_resolves(self):
        self.client.force_login(self.user)
        self.assertEqual(resolve(reverse('subscription')).func.view_class, views.SubscriptionView)
        response = self.client.get(reverse('subscription'))
        self.assertEqual(response.status_code, 200)

    def test_subscription_unauthorised(self):
        response = self.client.get(reverse('subscription'))
        self.assertEqual(response.status_code, 302)


