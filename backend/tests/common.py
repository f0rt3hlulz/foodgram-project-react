from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token


def create_users_api(admin_client):
    data = {
        'username': 'jean-mixin',
        'email': 'jean-mixin@foodgram.fake',
        'password': 'fo0dgr@mTest',
        'first_name': 'Jean',
        'last_name': 'Mixin',
        'is_superuser': False,
    }
    admin_client.post('/api/users/', data=data)
    user = get_user_model().objects.get(username=data['username'])
    data = {
        'username': 'jean-admin',
        'email': 'jean-admin@foodgram.fake',
        'password': 'fo0dgr@mTest',
        'first_name': 'Jean',
        'last_name': 'Admin',
        'is_superuser': True,
    }
    admin_client.post('/api/users/', data=data)
    admin = get_user_model().objects.get(username=data['username'])
    return user, admin


def auth_client(user):
    token = Token.objects.create(user=user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
    return client
