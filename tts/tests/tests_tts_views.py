import os

from django.conf import settings
from django.db.models import QuerySet
from django.test import TestCase
from django.urls import reverse

from tts.forms import TextToSpeechForm
from tts.models import AudioFile, UserAction
from users.models import CustomUser


class TextToSpeechViewTestCase(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create(
            username='Nike',
            auth0_id='google12313213',
            email='any@gmail.com',
            password='password',
            is_premium=False
        )

    def test_get_authenticated_connect(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('convert_text_to_speech'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tts/convert_text_to_speech.html')
        self.assertIsInstance(response.context['form'], TextToSpeechForm)

    def test_get_unauthenticated_connect(self):
        response = self.client.get(reverse('convert_text_to_speech'))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'tts/convert_text_to_speech.html')
        with self.assertRaises(TypeError):
            self.assertIsNone(response.context['form'])

    def test_post_text(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('convert_text_to_speech'), {'text': 'some text'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tts/convert_text_to_speech.html')
        self.assertTrue(response.context['form'].is_valid())
        self.assertTrue(response.context['audio_file_url'])
        self.assertEqual(response.context['audio_file_url'], '/media/some.mp3')
        self.assertTrue(response.context['output_file'])
        self.assertEqual(response.context['output_file'], 'some.mp3')
        self.assertTrue(AudioFile.objects.exists())
        self.assertTrue(UserAction.objects.exists())
        os.remove(os.path.join(settings.MEDIA_ROOT, 'some.mp3'))

    def common_file_upload(self, file_path):
        with open(file_path, 'rb') as file:
            self.client.force_login(self.user)
            response = self.client.post(
                reverse('convert_text_to_speech'),
                {'text_file': file}
            )
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'tts/convert_text_to_speech.html')
            self.assertTrue(response.context['form'].is_valid())
            self.assertTrue(response.context['audio_file_url'])
            self.assertEqual(response.context['audio_file_url'], '/media/output.mp3')
            self.assertTrue(response.context['output_file'])
            self.assertEqual(response.context['output_file'], 'output.mp3')
            self.assertTrue(AudioFile.objects.exists())
            self.assertTrue(UserAction.objects.exists())
            AudioFile.objects.filter(user=self.user).delete()

    def test_post_docx_file(self):
        self.common_file_upload('tts/tests/tests_files/output.docx')

    def test_post_pdf_file(self):
        self.common_file_upload('tts/tests/tests_files/output.pdf')

    def test_post_txt_file(self):
        self.common_file_upload('tts/tests/tests_files/output.txt')

    def test_post_users_limit(self):
        self.client.force_login(self.user)
        for _ in range(11):
            AudioFile.objects.create(user=self.user)
        response = self.client.post(reverse('convert_text_to_speech'), {'text': 'some text'})
        self.assertTrue(response.context['users_limit'])
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tts/convert_text_to_speech.html')
        self.assertTrue(response.context['form'].is_valid())
        self.assertIsNone(response.context['audio_file_url'])
        with self.assertRaises(KeyError):
            response.context['output_file']

    def test_post_invalid(self):
        self.client.force_login(self.user)
        with self.assertRaises(TypeError):
            response = self.client.post(reverse('convert_text_to_speech'), {})
            self.assertFalse(response.context['form'].is_valid())
            self.assertEqual(response.status_code, 404)
            self.assertTemplateNotUsed(response, 'tts/convert_text_to_speech.html')


class TtsFilesViewTestCase(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create(
            username='Nike',
            auth0_id='google12313213',
            email='any@gmail.com',
            password='password',
            is_premium=False
        )

    def test_get_authenticated_connect(self):
        self.client.force_login(self.user)
        for _ in range(3):
            AudioFile.objects.create(user=self.user)
        response = self.client.get(reverse('tts_files'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tts/tts_files.html')
        self.assertTrue(response.context['user_files'])
        self.assertIsInstance(response.context['user_files'], QuerySet)
        self.assertEqual(len(response.context['user_files']), 3)

    def test_get_unauthenticated_connect(self):
        response = self.client.get(reverse('tts_files'))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'tts/tts_files.html')
        with self.assertRaises(TypeError):
            self.assertIsNone(response.context['user_files'])


class UsersHistoryViewTestCase(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create(
            username='Nike',
            auth0_id='google12313213',
            email='any@gmail.com',
            password='password',
            is_premium=False
        )

    def test_get_authenticated_connect(self):
        self.client.force_login(self.user)
        for _ in range(3):
            UserAction.objects.create(user=self.user)
        response = self.client.get(reverse('history'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tts/history.html')
        self.assertTrue(response.context['user_actions'])
        self.assertIsInstance(response.context['user_actions'], QuerySet)
        self.assertEqual(len(response.context['user_actions']), 3)

    def test_get_unauthenticated_connect(self):
        response = self.client.get(reverse('history'))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'tts/history.html')
        with self.assertRaises(TypeError):
            self.assertIsNone(response.context['user_actions'])


# class AudioToTextViewTestCase(TestCase):
#     def setUp(self):
#         self.user = CustomUser.objects.create(
#             username='Nike',
#             auth0_id='google12313213',
#             email='any@gmail.com',
#             password='password',
#             is_premium=False
#         )
#
#     def test_get_authenticated_connect(self):
#         self.client.force_login(self.user)
#         response = self.client.get(reverse('stt'))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'tts/stt.html')
#         self.assertTrue(response.context['form'])
#
#     def test_get_unauthenticated_connect(self):
#         response = self.client.get(reverse('stt'))
#         self.assertEqual(response.status_code, 302)
#         self.assertTemplateNotUsed(response, 'tts/stt.html')
#         with self.assertRaises(TypeError):
#             self.assertTrue(response.context['form'])
#
#     def upload_audio(self, path):
#         self.client.force_login(self.user)
#         with open(path, 'rb') as file:
#             response = self.client.post(reverse('stt'), {'audiofile': file})
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'tts/stt.html')
#         self.assertTrue(response.context['form'])
#         self.assertTrue(response.context['form'].is_valid)
#         self.assertTrue(response.context['text'])
#         self.assertEqual(response.context['text'], 'some text')
#         try:
#             os.remove('some.wav')
#         except:
#             pass
#
#     def test_post_wav(self):
#         self.upload_audio(path='tts/tests/tests_files/some.wav')
#
#     def test_post_mp3(self):
#         self.upload_audio(path='tts/tests/tests_files/some.mp3')
#
#     def test_post_invalid(self):
#         self.client.force_login(self.user)
#         with self.assertRaises(TypeError):
#             response = self.client.post(reverse('stt'), {})
#             self.assertFalse(response.context['form'].is_valid())
#             self.assertEqual(response.status_code, 404)
#             self.assertTemplateNotUsed(response, 'tts/stt.html')
