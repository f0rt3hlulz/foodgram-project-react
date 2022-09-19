import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


class Test00UserRegistration:
    signup_endpoint = '/api/users/'
    token_endpoint = '/api/auth/token/login/'

    @pytest.mark.django_db(transaction=True)
    def test_00_00_post_signup_without_payload(self, client):
        request_type = 'POST'
        response = client.post(self.signup_endpoint)
        assert (
            response.status_code != 404
        ), f'Страница `{self.signup_endpoint}` не найдена, проверьте этот адрес в *urls.py*'

        code = 400
        assert response.status_code == code, (
            f'Проверьте, что при {request_type} запросе к {self.signup_endpoint} без параметров '
            f'не создается пользователь и возвращается статус {code}.'
        )

        response_json = response.json()
        empty_fields = [
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
        ]
        for field in empty_fields:
            assert field in response_json.keys() and isinstance(
                response_json[field], list
            ), (
                f'Проверьте, что при {request_type} запросе к {self.signup_endpoint} без параметров '
                f'в ответе есть сообщение о том, какие поля заполенены неправильно.'
            )

    @pytest.mark.django_db(transaction=True)
    def test_00_01_post_signup_with_invalid_payload(self, client):
        request_type = 'POST'
        invalid_email = 'jean-mixin-01'
        invalid_username = 'jean-mixin-01@foodgram.fake'
        first_name = 'Jean'
        last_name = 'Mixin'
        password = 'fo0dgr@mTest'
        invalid_data = {
            'email': invalid_email,
            'username': invalid_username,
            'first_name': first_name,
            'last_name': last_name,
            'password': password,
        }
        response = client.post(self.signup_endpoint, data=invalid_data)
        assert (
            response.status_code != 404
        ), f'Страница {self.signup_endpoint} не найдена, проверьте этот адрес в *urls.py*'

        code = 400
        assert response.status_code == code, (
            f'Проверьте, что при {request_type} запросе к {self.signup_endpoint} с невалидными данными '
            f'не создается пользователь и возвращается статус {code}.'
        )

        response_json = response.json()
        invalid_fields = ['email']
        for field in invalid_fields:
            assert field in response_json.keys() and isinstance(
                response_json[field], list
            ), (
                f'Проверьте, что при {request_type} запросе к {self.signup_endpoint} с невалидными параметрами '
                f'в ответе есть сообщение о том, какие поля заполенены неправильно.'
            )

        valid_email = 'jean-mixin-02@foodgram.fake'
        invalid_data = {
            'email': valid_email,
            'first_name': first_name,
            'last_name': last_name,
            'password': password,
        }
        response = client.post(self.signup_endpoint, data=invalid_data)
        assert response.status_code == code, (
            f'Проверьте, что при {request_type} запросе к {self.signup_endpoint} без username '
            f'нельзя создать пользователя и возвращается статус {code}.'
        )

    @pytest.mark.django_db(transaction=True)
    def test_00_02_post_signup_with_valid_payload(self, client):
        request_type = 'POST'
        valid_email = 'jean-mixin-03@foodgram.fake'
        valid_username = 'jean-mixin-03'
        first_name = 'Jean'
        last_name = 'Mixin'
        password = 'fo0dgr@mTest'
        valid_data = {
            'email': valid_email,
            'username': valid_username,
            'first_name': first_name,
            'last_name': last_name,
            'password': password,
        }
        response = client.post(self.signup_endpoint, data=valid_data)
        assert (
            response.status_code != 404
        ), f'Страница {self.signup_endpoint} не найдена, проверьте этот адрес в *urls.py*'

        code = 201
        assert response.status_code == code, (
            f'Проверьте, что при {request_type} запросе к {self.signup_endpoint} с валидными данными '
            f'создается пользователь и возвращается статус {code}.'
        )

        response_json = response.json()
        valid_fields = ['username', 'email', 'first_name', 'last_name']
        for field in valid_fields:
            assert field in response_json.keys(), (
                f'Проверьте, что при {request_type} запросе к {self.signup_endpoint} с валидными данными '
                f'создается пользователь и возвращается статус {code}.'
            )
        new_user = User.objects.filter(email=valid_email)
        assert new_user.exists(), (
            f'Проверьте, что при {request_type} запросе к {self.signup_endpoint} с валидными данными '
            f'создается пользователь и возвращается статус {code}.'
        )

        new_user.delete()

    @pytest.mark.django_db(transaction=True)
    def test_00_03_post_signup_with_restricted_payload(self, client):
        request_type = 'POST'
        invalid_username = 'me'
        email = 'jean-mixin-04@foodgram.fake'
        first_name = 'Jean'
        last_name = 'Mixin'
        password = 'fo0dgr@mTest'
        valid_data = {
            'username': invalid_username,
            'email': email,
            'password': password,
            'first_name': first_name,
            'last_name': last_name,
            'is_superuser': False,
        }
        response = client.post(self.signup_endpoint, data=valid_data)
        code = 400
        assert response.status_code == code, (
            f'Проверьте, что при {request_type} запросе к {self.signup_endpoint} '
            f'нельзя создать пользователя с username = "me" и возвращается статус {code}.'
        )

    @pytest.mark.django_db(transaction=True)
    def test_00_04_post_signup_with_duplicate_payload(self, client):
        request_type = 'POST'
        username_1 = 'jean-mixin-05'
        username_2 = 'jean-mixin-06'
        email_1 = 'jean-mixin-05@foodgram.fake'
        email_2 = 'jean-mixin-06@foodgram.fake'
        password_1 = 'fo0dgr@mTest'
        password_2 = 'fo0dgr@mTest'
        first_name_1 = 'Jean'
        first_name_2 = 'Jean'
        last_name_1 = 'Mixin'
        last_name_2 = 'Mixin'
        valid_data = {
            'username': username_1,
            'email': email_1,
            'password': password_1,
            'first_name': first_name_1,
            'last_name': last_name_1,
            'is_superuser': False,
        }
        response = client.post(self.signup_endpoint, data=valid_data)
        code = 201
        assert response.status_code == code, (
            f'Проверьте, что при {request_type} запросе к {self.signup_endpoint} '
            f'можно создать пользователя с валидными данными и возвращается статус {code}.'
        )

        duplicate_email_data = {
            'username': username_2,
            'email': email_1,
            'password': password_2,
            'first_name': first_name_2,
            'last_name': last_name_2,
            'is_superuser': False,
        }
        response = client.post(self.signup_endpoint, data=duplicate_email_data)
        code = 400
        assert response.status_code == code, (
            f'Проверьте, что при {request_type} запросе к {self.signup_endpoint} нельзя создать '
            f'пользователя, email которого уже зарегистрирован и возвращается статус {code}.'
        )

        duplicate_username_data = {
            'email': email_2,
            'username': username_1,
        }
        duplicate_username_data = {
            'username': username_1,
            'email': email_2,
            'password': password_2,
            'first_name': first_name_2,
            'last_name': last_name_2,
            'is_superuser': False,
        }
        response = client.post(
            self.signup_endpoint, data=duplicate_username_data
        )
        assert response.status_code == code, (
            f'Проверьте, что при {request_type} запросе к {self.signup_endpoint} нельзя создать '
            f'пользователя, username которого уже зарегистрирован и возвращается статус {code}.'
        )

    @pytest.mark.django_db(transaction=True)
    def test_00_05_post_obtain_token_with_invalid_payload(self, client):
        request_type = 'POST'
        username = 'jean-mixin-07'
        email = 'jean-mixin-07@foodgram.fake'
        password = 'fo0dgr@mTest'
        first_name = 'Jean'
        last_name = 'Mixin'

        response = client.post(self.token_endpoint)
        assert (
            response.status_code != 404
        ), f'Страница `{self.token_endpoint}` не найдена, проверьте этот адрес в *urls.py*'

        code = 400
        assert response.status_code == code, (
            f'Проверьте, что при {request_type} запросе к {self.token_endpoint} без параметров '
            f'возвращается статус {code}.'
        )

        invalid_data = {'password': password}
        response = client.post(self.token_endpoint, data=invalid_data)
        assert response.status_code == code, (
            f'Проверьте, что при {request_type} запросе к {self.token_endpoint} без email '
            f'возвращается статус {code}.'
        )

        invalid_data = {
            'email': 'jean-mixin-08@foodgram.fake',
            'password': password,
        }
        response = client.post(self.token_endpoint, data=invalid_data)
        code = 400
        assert response.status_code == code, (
            f'Проверьте, что при {request_type} запросе к {self.token_endpoint} с несуществующим email '
            f'возвращается статус {code}.'
        )

        valid_data = {
            'username': username,
            'email': email,
            'password': password,
            'first_name': first_name,
            'last_name': last_name,
            'is_superuser': False,
        }
        response = client.post(self.signup_endpoint, data=valid_data)
        code = 201
        assert response.status_code == code, (
            f'Проверьте, что при {request_type} запросе к {self.signup_endpoint} с валидными данными '
            f'создается пользователь и возвращается статус {code}.'
        )

        invalid_password = 'Testfo0dgr@m'
        invalid_data = {'email': email, 'password': invalid_password}
        response = client.post(self.token_endpoint, data=invalid_data)
        code = 400
        assert response.status_code == code, (
            f'Проверьте, что при {request_type} запросе к {self.token_endpoint} с валидным email '
            f'но невалидным password, возвращается статус {code}.'
        )
