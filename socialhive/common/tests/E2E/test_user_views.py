import pytest
from rest_framework import status

from socialhive.conftest import TestBase


@pytest.mark.django_db
class TestUsersViews(TestBase):
    USERS_URL = '/api/v1/users/'

    def test_change_password_success(self):
        data = {
            'old_password': 'test_password',
            'new_password': 'newtestpass',
            'new_password_confirmation': 'newtestpass'
        }

        response = self.api_client.post(f"{self.USERS_URL}change-password/", data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert self.user.check_password(data['new_password'])

    def test_change_password_incorrect_old_password(self):
        data = {
            'old_password': 'wrongpass',
            'new_password': 'newtestpass',
            'new_password_confirmation': 'newtestpass'
        }
        self.api_client.force_authenticate(user=self.user)
        response = self.api_client.post(f"{self.USERS_URL}change-password/", data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_change_password_mismatched_new_passwords(self):
        data = {
            'old_password': 'test_password',
            'new_password': 'newtestpass',
            'new_password_confirmation': 'mismatchedpass'
        }
        self.api_client.force_authenticate(user=self.user)
        response = self.api_client.post(f"{self.USERS_URL}change-password/", data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "New password and confirmation don't match." in response.data["error_message"]

    def test_change_password_same_old_and_new_passwords(self):
        data = {
            'old_password': 'test_password',
            'new_password': 'test_password',
            'new_password_confirmation': 'test_password'
        }
        self.api_client.force_authenticate(user=self.user)
        response = self.api_client.post(f"{self.USERS_URL}change-password/", data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "New password can't be the same as the old one." in response.data['error_message']

    def test_change_password_similar_old_and_new_passwords(self):
        data = {
            'old_password': 'test_password',
            'new_password': 'testpass123',
            'new_password_confirmation': 'testpass123'
        }
        self.api_client.force_authenticate(user=self.user)
        response = self.api_client.post(f"{self.USERS_URL}change-password/", data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "New password can't be too similar to the old one." in response.data['error_message']
