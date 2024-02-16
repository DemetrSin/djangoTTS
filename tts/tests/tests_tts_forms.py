from django.test import TestCase

from tts.forms import AudioToTextForm, TextToSpeechForm
from tts.models import AudioFile
from users.models import CustomUser


class TextToSpeechFormTestCase(TestCase):

    def setUp(self):
        self.premium_user = CustomUser.objects.create(
            username='Nike',
            is_premium=True
        )
        self.non_premium_user = CustomUser.objects.create(
            username='Nik',
            is_premium=False
        )

    def test_valid_form(self):
        form_without_text = TextToSpeechForm(
            {
                'text_file': 'some.pdf'
            }
        )
        form_with_text = TextToSpeechForm(
            {
                'text': 'Some text',
            }
        )
        self.assertTrue(form_without_text.is_valid())
        self.assertTrue(form_with_text.is_valid())

    def test_invalid_form(self):
        form = TextToSpeechForm()
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 0)

    def test_premium_user_text_length(self):
        form = TextToSpeechForm(user=self.premium_user)
        self.assertEqual(form.fields['text'].validators[-1].limit_value, 10000)
        self.assertEqual(
            form.fields['text'].validators[-1].message,
            "Even with premium status you can't input more than 10000 symbols"
        )

    def test_non_premium_user_text_length(self):
        form = TextToSpeechForm(user=self.non_premium_user)
        self.assertEqual(
            form.fields['text'].validators[-1].message,
            "Without premium status you can't input more than 1000 symbols"
        )

    def test_meta_fields(self):
        form = TextToSpeechForm()
        self.assertEqual(form.Meta.model, AudioFile)
        self.assertEqual(form.Meta.fields, ['text', 'text_file'])


class AudioToTextFormTestCase(TestCase):

    def test_valid_form(self):
        form = AudioToTextForm(
            {
                'audiofile': 'some.mp3'
            }
        )
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = AudioToTextForm()
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 0)

    def test_meta_fields(self):
        form = AudioToTextForm()
        self.assertEqual(form.Meta.model, AudioFile)
        self.assertEqual(form.Meta.fields, ['audiofile'])
