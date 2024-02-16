from django.test import Client, TestCase
from users.models import CustomUser
from django.urls import reverse


class TextToSpeechViewTestCase(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create(
            username='Nike',
            auth0_id='google12313213',
            email='any@gmail.com',
            password='password',
            is_premium=False
        )
        self.client.force_login(self.user)

    def test_get(self):
        response = self.client.get(reverse('convert_text_to_speech'))
        self.assertEqual(response.status_code, 200)
