import pytest
from rest_framework.test import APIClient

from socialhive.common.tests.factories import UserFactory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return UserFactory()


@pytest.fixture
def get_session(user, api_client):
    api_client.force_authenticate(user=user)
    return api_client, user


class TestBase:
    @pytest.fixture(autouse=True)
    def setup(self, get_session):
        self.api_client, self.user = get_session
        return api_client, user
