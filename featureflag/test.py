from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch
from .models import User

class FeatureFlagTestCase(APITestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create(name="Test User", age=25, address="Test Address")

    @patch('featureflag.views.r')
    def test_get_feature_flag_value(self, mock_redis):
        # Mock the Redis object to avoid actual connection
        mock_redis.get.return_value = "enabled"

        url = reverse('feature_flag')
        response = self.client.get(url, {'key': 'feature1'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'feature1': 'enabled'})

    @patch('featureflag.views.r')
    def test_user_operations_post(self, mock_redis):
        # Mock the Redis object to avoid actual connection
        mock_redis.get.return_value = "1"

        url = reverse('user_operations')
        data = {'name': 'John Doe', 'age': 30, 'address': '123 Main St'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 2)  # Check if a new user is created

    @patch('featureflag.views.r')
    def test_user_operations_get(self, mock_redis):
        # Mock the Redis object to avoid actual connection
        mock_redis.get.return_value = "1"

        url = reverse('user_operations')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['user_list']), 1)  # Check if the response contains the user list

    @patch('featureflag.views.r')
    def test_edit_delete_user_put(self, mock_redis):
        # Mock the Redis object to avoid actual connection
        mock_redis.get.return_value = "1"

        url = reverse('edit_delete_user', args=[self.user.id])
        data = {'name': 'Updated User', 'age': 35, 'address': '456 Elm St'}
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, 'Updated User')  # Check if user data is updated

    @patch('featureflag.views.r')
    def test_edit_delete_user_delete(self, mock_redis):
        # Mock the Redis object to avoid actual connection
        mock_redis.get.return_value = "1"

        url = reverse('edit_delete_user', args=[self.user.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 0)  # Check if the user is deleted
