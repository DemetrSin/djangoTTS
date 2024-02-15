from datetime import datetime

from django.test import TestCase
from tts.models import AudioFile, UserAction
from users.models import CustomUser


class AudioFileTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='Nike',
            auth0_id='google12313213',
            email='any@gmail.com',
            password='password',
            is_premium=False
        )
        self.audiofile = AudioFile.objects.create(
            user=self.user,
            text='Some text',
            text_file='text_files/some.txt',
            filename='some.txt',
            audiofile='some.mp3',
            zipfile='some.zip'
        )

    def test_setup_object(self):
        self.assertIsInstance(self.audiofile.user, CustomUser)
        self.assertIsInstance(self.audiofile.created_at, datetime)
        self.assertIsNotNone(self.audiofile.created_at)
        self.assertEqual(self.audiofile.text, 'Some text')
        self.assertEqual(self.audiofile.text_file, 'text_files/some.txt')
        self.assertEqual(self.audiofile.filename, 'some.txt')
        self.assertEqual(self.audiofile.audiofile, 'some.mp3')
        self.assertEqual(self.audiofile.zipfile, 'some.zip')

    def test_empty_audiofile(self):
        audiofile = AudioFile.objects.create(user=self.user)
        self.assertIsNone(audiofile.text)
        self.assertFalse(audiofile.text_file)
        self.assertFalse(audiofile.filename)
        self.assertFalse(audiofile.audiofile)
        self.assertFalse(audiofile.zipfile)

    def test_wrong_created_at(self):
        with self.assertRaises(TypeError):
            AudioFile.objects.create(user=self.user, created_at=int(datetime))

    def test_string_representation(self):
        audiofile = AudioFile.objects.create(user=self.user, filename='some.txt')
        self.assertEqual(str(audiofile), "2 > Nike > some.txt")


class UserActionTestCase(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='Nike',
            auth0_id='google12313213',
            email='any@gmail.com',
            password='password',
            is_premium=False
        )
        self.user_action = UserAction.objects.create(user=self.user, action='Some action')

    def test_setup_object(self):
        self.assertIsInstance(self.user_action.user, CustomUser)
        self.assertEqual(self.user_action.action, 'Some action')
        self.assertIsInstance(self.user_action.timestamp, datetime)
        self.assertIsNotNone(self.user_action.timestamp, datetime)

    def test_string_representation(self):
        action = UserAction.objects.create(user=self.user)
        self.assertEqual(str(action), '1 Nike google12313213')

    def test_wrong_timestamp(self):
        with self.assertRaises(TypeError):
            UserAction.objects.create(user=self.user, created_at=int(datetime))
