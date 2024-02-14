from datetime import datetime, timedelta

from django.core.exceptions import ValidationError
from django.test import TestCase
from users.models import CustomUser, AnonymousFiles, Subscription
from django.contrib.auth.hashers import check_password


class CustomUserTestCase(TestCase):
    def setUp(self):
        CustomUser.objects.create_user(
            username='Nike',
            is_premium=False,
            auth0_id='google235429-12',
            email='any@gmail.com'
        )
        CustomUser.objects.create_superuser(
            username='admin',
            is_premium=False,
            is_staff=True,
            is_superuser=True,
            email=False,
            password='something1234'
        )

    def test_create_user(self):
        user = CustomUser.objects.get(username='Nike')
        self.assertFalse(user.is_premium)
        self.assertTrue(user.auth0_id)
        self.assertEqual(user.email, 'any@gmail.com')

    def test_createsuperuser(self):
        superuser = CustomUser.objects.get(username='admin')
        self.assertFalse(superuser.is_premium)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertEqual(superuser.email, '')
        self.assertTrue(check_password('something1234', superuser.password))


class AnonymousFilesTestCase(TestCase):
    def setUp(self) -> None:
        AnonymousFiles.objects.create(
            text='Some text here',
            audiofile='m.mp3',
            created_at='Feb. 14, 2024, 2:42 p.m.'
        )

    def test_create_anonymous_file(self):
        anonymous_file = AnonymousFiles.objects.get(id=1)
        self.assertEqual(anonymous_file.text, 'Some text here')
        self.assertEqual(anonymous_file.audiofile, 'm.mp3')
        self.assertTrue(anonymous_file.created_at)
        self.assertIsInstance(anonymous_file.created_at, datetime)

    def test_invalid_anonymous_text(self):
        with self.assertRaises(ValidationError):
            invalid_file = AnonymousFiles.objects.create(text='')
            invalid_file.full_clean()

    def test_invalid_anonymous_audiofile(self):
        with self.assertRaises(ValidationError):
            invalid_file = AnonymousFiles.objects.create(audiofile='')
            invalid_file.full_clean()

    def test_invalid_anonymous_created_at(self):
        with self.assertRaises(ValidationError):
            invalid_file = AnonymousFiles()
            invalid_file.full_clean()


class SubscriptionTestCase(TestCase):

    def setUp(self) -> None:
        self.user = CustomUser.objects.create_user(
            username='Nike',
            is_premium=False,
            auth0_id='google235429-12',
            email='any@gmail.com'
        )
        start_date = datetime.now()
        end_date = start_date + timedelta(days=30)
        self.subs = Subscription.objects.create(
            user=self.user,
            start_date=start_date,
            end_date=end_date,
            is_active=True,
            payment_status=True
        )

    def test_create_subscription(self):
        self.assertIsInstance(self.subs.start_date, datetime)
        self.assertIsInstance(self.subs.end_date, datetime)
        self.assertTrue(self.subs.is_active)
        self.assertTrue(self.subs.payment_status)

    def test_invalid_user(self):
        invalid_sub = Subscription(user=None)
        with self.assertRaises(ValidationError):
            invalid_sub.full_clean()

    def test_missing_end_date(self):
        invalid_sub = Subscription(user=self.user)
        with self.assertRaises(ValidationError):
            invalid_sub.full_clean()

    def test_invalid_payment_status(self):
        invalid_sub = Subscription(user=self.user, end_date=datetime.now(), payment_status="invalid")
        with self.assertRaises(ValidationError):
            invalid_sub.full_clean()
