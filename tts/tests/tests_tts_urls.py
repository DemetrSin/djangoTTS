from django.test import TestCase
from django.urls import resolve, reverse

from users.models import CustomUser
from tts import views


class TtsUrlsTestCase(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(username='Nick')

    def test_convert_text_to_speech_url_resolves(self):
        self.client.force_login(self.user)
        self.assertEqual(resolve(reverse('convert_text_to_speech')).func.view_class, views.TextToSpeechView)
        response = self.client.get(reverse('convert_text_to_speech'))
        self.assertEqual(response.status_code, 200)

    def test_convert_text_to_speech_unauthorised(self):
        response = self.client.get(reverse('convert_text_to_speech'))
        self.assertEqual(response.status_code, 302)

    def test_tts_files_url_resolves(self):
        self.client.force_login(self.user)
        self.assertEqual(resolve(reverse('tts_files')).func.view_class, views.TtsFilesView)
        response = self.client.get(reverse('tts_files'))
        self.assertEqual(response.status_code, 200)

    def test_tts_files_unauthorised(self):
        response = self.client.get(reverse('tts_files'))
        self.assertEqual(response.status_code, 302)

    def test_history_url_resolves(self):
        self.client.force_login(self.user)
        self.assertEqual(resolve(reverse('history')).func.view_class, views.UsersHistoryView)
        response = self.client.get(reverse('history'))
        self.assertEqual(response.status_code, 200)

    def test_history_unauthorised(self):
        response = self.client.get(reverse('history'))
        self.assertEqual(response.status_code, 302)

    def test_stt_resolves(self):
        self.client.force_login(self.user)
        self.assertEqual(resolve(reverse('stt')).func.view_class, views.AudioToTextView)
        response = self.client.get(reverse('stt'))
        self.assertEqual(response.status_code, 200)

    def test_stt_unauthorised(self):
        response = self.client.get(reverse('stt'))
        self.assertEqual(response.status_code, 302)
