import pytest


@pytest.fixture
def admin(django_user_model):
    return django_user_model.objects.create_superuser(
        username='jean-admin',
        email='jean-admin@foodgram.fake',
        password='fo0dgr@mTest',
        first_name='Jean',
        last_name='Admin',
        is_superuser=True,
    )


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(
        username='jean-mixin',
        email='jean-mixin@foodgram.fake',
        password='fo0dgr@mTest',
        first_name='Jean',
        last_name='Mixin',
        is_superuser=False,
    )


@pytest.fixture
def token_admin(admin):
    from rest_framework.authtoken.models import Token

    token = Token.objects.create(user=admin)

    return {
        'access': str(token.key),
    }


@pytest.fixture
def admin_client(token_admin):
    from rest_framework.test import APIClient

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token_admin["access"]}')
    return client


@pytest.fixture
def token_user(user):
    from rest_framework.authtoken.models import Token

    token = Token.objects.create(user=user)

    return {
        'access': str(token.key),
    }


@pytest.fixture
def user_client(token_user):
    from rest_framework.test import APIClient

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token_user["access"]}')
    return client
