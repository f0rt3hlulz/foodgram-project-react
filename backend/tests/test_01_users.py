import pytest
from django.contrib.auth import get_user_model


class Test01UserAPI:
    users_endpoint = '/api/users/'
    user_endpoint = '/api/users/{id}'
    current_user_endpoint = '/api/users/me'

    @pytest.mark.django_db(transaction=True)
    def test_01_00_get_users_id_without_auth(self, client, user):
        request_type = 'GET'
        response = client.get(f'/api/users/{user.id}/')
        code = 404
        assert (
            response.status_code != code
        ), f'Страница {self.user_endpoint} не найдена, проверьте этот адрес в *urls.py*'

        code = 200
        assert response.status_code == code, (
            f'Проверьте, что при {request_type} запросе к {self.user_endpoint} без токена авторизации '
            f'возвращается статус {code}.'
        )

    @pytest.mark.django_db(transaction=True)
    def test_01_01_get_current_user_without_auth(self, client):
        request_type = 'GET'
        response = client.get('/api/users/me/')
        code = 404
        assert (
            response.status_code != code
        ), f'Страница {self.current_user_endpoint} не найдена, проверьте этот адрес в *urls.py*'

        code = 401
        assert response.status_code == code, (
            f'Проверьте, что при {request_type} запросе к {self.current_user_endpoint} без токена авторизации '
            f'возвращается статус {code}.'
        )

    @pytest.mark.django_db(transaction=True)
    def test_01_02_get_users_with_auth(self, user_client, user):
        request_type = 'GET'
        response = user_client.get('/api/users/')
        code = 404
        assert (
            response.status_code != code
        ), f'Страница {self.users_endpoint} не найдена, проверьте этот адрес в *urls.py*'

        code = 200
        assert response.status_code == code, (
            f'Проверьте, что при {request_type} запросе к {self.users_endpoint} с токеном авторизации '
            f'возвращается статус {code}.'
        )

        response_param = 'count'
        response_data = response.json()
        assert response_param in response_data, (
            f'Проверьте, что при {request_type} запросе к {self.users_endpoint} возвращаются данные с пагинацией. '
            f'Не найден параметр {response_param}.'
        )

        response_param = 'next'
        assert response_param in response_data, (
            f'Проверьте, что при {request_type} запросе к {self.users_endpoint} возвращаются данные с пагинацией. '
            f'Не найден параметр {response_param}.'
        )

        response_param = 'previous'
        assert response_param in response_data, (
            f'Проверьте, что при {request_type} запросе к {self.users_endpoint} возвращаются данные с пагинацией. '
            f'Не найден параметр {response_param}.'
        )

        response_param = 'results'
        assert response_param in response_data, (
            f'Проверьте, что при {request_type} запросе к {self.users_endpoint} возвращаются данные с пагинацией. '
            f'Не найден параметр {response_param}.'
        )

        response_param = 'count'
        assert response_data[response_param] == 1, (
            f'Проверьте, что при {request_type} запросе к {self.users_endpoint} возвращаются данные с пагинацией. '
            f'Ошибка в значении параметра {response_param}.'
        )

        response_param = 'results'
        assert type(response_data[response_param]) == list, (
            f'Проверьте, что при {request_type} запросе к {self.users_endpoint} возвращаются данные с пагинацией. '
            f'Тип параметра {response_param} должен быть list.'
        )

        response_param = 'results'
        assert (
            len(response_data[response_param]) == 1
            and response_data[response_param][0].get('username')
            == user.username
            and response_data[response_param][0].get('email') == user.email
        ), (
            f'Проверьте, что при {request_type} запросе к {self.users_endpoint} возвращаются данные с пагинацией. '
            f'Ошибка в значении параметра {response_param}.'
        )

    @pytest.mark.django_db(transaction=True)
    def test_01_03_post_users_with_admin_auth(self, admin_client, admin):
        empty_data = {}
        request_type = 'POST'
        response = admin_client.post('/api/users/', data=empty_data)
        code = 400
        assert response.status_code == code, (
            f'Проверьте, что при {request_type} запросе к {self.users_endpoint} с пустыми данными '
            f'возвращается статус {code}.'
        )

        no_email_data = {
            'username': 'jean-mixin-01',
            'password': 'fo0dgr@mTest',
            'first_name': 'Jean',
            'last_name': 'Mixin',
            'is_superuser': False,
        }
        response = admin_client.post('/api/users/', data=no_email_data)
        code = 400
        assert response.status_code == 400, (
            f'Проверьте, что при {request_type} запросе к {self.users_endpoint} без email '
            f'возвращается статус {code}.'
        )

        no_username_data = {
            'email': 'jean-mixin-02@foodgram.fake',
            'password': 'fo0dgr@mTest',
            'first_name': 'Jean',
            'last_name': 'Mixin',
            'is_superuser': False,
        }
        response = admin_client.post('/api/users/', data=no_username_data)
        code = 400
        assert response.status_code == code, (
            f'Проверьте, что при {request_type} запросе к {self.users_endpoint} без username '
            f'возвращается статус {code}.'
        )

        duplicate_email = {
            'username': 'jean-mixin-03',
            'password': 'fo0dgr@mTest',
            'first_name': 'Jean',
            'last_name': 'Mixin',
            'is_superuser': False,
            'email': admin.email,
        }
        response = admin_client.post('/api/users/', data=duplicate_email)
        code = 400
        assert response.status_code == code, (
            f'Проверьте, что при {request_type} запросе к {self.users_endpoint} с уже существующим email '
            f'возвращается статус {code}. Email должен быть уникальный у каждого прользователя.'
        )

        duplicate_username = {
            'email': 'jean-mixin-04@foodgram.fake',
            'password': 'fo0dgr@mTest',
            'first_name': 'Jean',
            'last_name': 'Mixin',
            'is_superuser': False,
            'username': admin.username,
        }
        response = admin_client.post('/api/users/', data=duplicate_username)
        code = 400
        assert response.status_code == code, (
            f'Проверьте, что при {request_type} запросе к {self.users_endpoint} с уже существующим username '
            f'возвращается статус {code}. Username должен быть уникальный у каждого прользователя.'
        )

        valid_data = {
            'username': 'jean-mixin-05',
            'email': 'jean-mixin-05@foodgram.fake',
            'password': 'fo0dgr@mTest',
            'first_name': 'Jean',
            'last_name': 'Mixin',
            'is_superuser': False,
        }
        response = admin_client.post('/api/users/', data=valid_data)
        response_data = response.json()
        code = 201
        assert response.status_code == code, (
            f'Проверьте, что при {request_type} запросе к {self.users_endpoint} с правильными данными '
            f'возвращается статус {code}.'
        )

        request_type = 'GET'
        response_param = 'first_name'
        assert (
            response_data.get(response_param) == valid_data[response_param]
        ), (
            f'Проверьте, что при {request_type} запросе к {self.users_endpoint} с правильными данными '
            f'возвращается {response_param}.'
        )

        response_param = 'last_name'
        assert (
            response_data.get(response_param) == valid_data[response_param]
        ), (
            f'Проверьте, что при {request_type} запросе к {self.users_endpoint} с правильными данными '
            f'возвращается {response_param}.'
        )

        response_param = 'username'
        assert (
            response_data.get(response_param) == valid_data[response_param]
        ), (
            f'Проверьте, что при {request_type} запросе к {self.users_endpoint} с правильными данными '
            f'возвращается {response_param}.'
        )

        response_param = 'email'
        assert (
            response_data.get(response_param) == valid_data[response_param]
        ), (
            f'Проверьте, что при {request_type} запросе к {self.users_endpoint} с правильными данными '
            f'возвращается {response_param}.'
        )

        User = get_user_model()
        users = User.objects.all()
        assert get_user_model().objects.count() == users.count(), (
            f'Проверьте, что при {request_type} запросе к {self.users_endpoint} '
            f'создаются пользователи.'
        )

        response = admin_client.get('/api/users/')
        response_data = response.json()
        response_param = 'results'
        assert len(response_data[response_param]) == users.count(), (
            f'Проверьте, что при {request_type} запросе к {self.users_endpoint} возвращаются данные с пагинацией. '
            f'Ошибка в значении параметра {response_param}.'
        )
