from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse


class UserRegistrationTest(TestCase):
    """
    Testing if user was registered successfully.
    """
    def test_user_registration(self):
        url = reverse('user_registration')
        response = self.client.post(url, {
            'username': 'Test',
            'password': 'password123',
            'repeat_password': 'password123',
            'email': 'test@example.com'
        })

        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.filter(username='Test').exists())


class UserLoginTest(TestCase):
    """
    Testing if user can log in successfully.
    """
    def setUp(self):
        self.user = User.objects.create_user(
            username='test',
            password='password123'
        )

    def test_user_login(self):
        url = reverse('token_obtain_pair')
        response = self.client.post(url, {
            'username': 'test',
            'password': 'password123',
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)

