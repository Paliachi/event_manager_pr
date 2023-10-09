from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.models import User
from django.urls import reverse

from .models import Event


class EventCRUDTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='person',
            password='password123'
        )
        self.refresh = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh.access_token)

        self.event = Event.objects.create(
            title='Test',
            description='Test description.',
            registration_end_date='2023-10-08',
            participants_quantity=60,
            organizator_user_id=self.user
        )

    def test_create_event(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        url = reverse('create_event')
        response = self.client.post(url, {
            'title': 'My Event',
            'description': 'This is my event',
            'registration_end_date': '2023-10-08',
            'participants_quantity': 10
        })

        self.assertEqual(response.status_code, 201)

    def test_list_user_events(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        url = reverse('user_events_list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_list_events(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        url = reverse('events_list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_update_event(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        url = reverse('update_event', args=[self.event.id])
        response = self.client.patch(url, {
            'title': 'Updated event',
            'description': 'Test Updates',
            'registration_end_date': '2023-10-10',
            'participants_quantity': 15
        })

        self.assertEqual(response.status_code, 200)



