import json
import uuid
import pytest
from django.urls import reverse

from . import models


@pytest.fixture
def test_password():
    return 'strong-test-pass'


@pytest.fixture
def create_bot_user(db, django_user_model, test_password):
    def make_user(**kwargs):
        if 'username' not in kwargs:
            kwargs['username'] = str(uuid.uuid4())
        return models.UserBot.objects.create(id=1234567, **kwargs)

    return make_user


@pytest.mark.django_db
def test_bot_user_auth(client, create_bot_user):
    user = create_bot_user(first_name='someone')
    url = reverse('userbot-auth')
    response = client.post(url, data=json.dumps({'id': user.id}), content_type="application/json")
    assert response.status_code == 200
