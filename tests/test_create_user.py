import allure
import requests
from data import *
from urls import *
import pytest


class TestCreateUser:
    @allure.title('Проверка успешной регистрации пользователя с валидными данными')
    @allure.description('Аккаунт создается с помощью учетных данных пользователей, которые генерируются библиотекой Faker и удаляется из базы данных'
                        'после теста. В ответе проверяются код и тело, и получение accessToken и refreshToken')
    def test_create_user_new_account_success(self):
        payload = {
            'email': create_random_email(),
            'password': create_random_password(),
            'name': create_random_username()
        }

        response = requests.post(Urls.user_register,data=payload)
        deserials = response.json()
        assert response.status_code ==200
        assert deserials['success'] is True
        assert 'accessToken' in deserials.keys()
        assert 'refreshToken' in deserials.keys()
        assert deserials['user']['email'] == payload['email']
        assert deserials['user']['name'] == payload['name']

        access_token = deserials['accessToken']
        requests.delete(Urls.user_delete, headers={'Authorization': access_token})

    @allure.title('Проверка ответа на запрос регистрации пользователя который уже зарегистрирован')
    @allure.description('Аккаунт создается с помощью учетных данных зарегистрированного пользователя.'
                        'Если аккаунт создастся, то он удаляется из базы данных после теста.')
    def test_create_user_account_sent_failed(self):
        payload = {
            'email': UsersData.email,
            'password': create_random_password(),
            'name': create_random_username()
        }
        response = requests.post(Urls.user_register, data=payload)
        assert response.status_code == 403 and response.json() == {'success': False, 'message': 'User already exists'}

    @allure.title('Проверка ответа на запрос регистрации пользователя когда не заполнено одно из обязательных полей')
    @allure.description('Выполняем три теста где не заполнено одно из полей — email, password или name.'
                        'Если аккаунт создастся, то он удаляется из базы данных после теста.')
    @pytest.mark.parametrize('credentials', UsersData.credentials_with_empty_field)
    def test_create_user_the_field_is_not_filled_in_failed(self, credentials):
        response = requests.post(Urls.user_register, data=credentials)
        assert (response.status_code == 403 and response.json() == {'success': False, 'message': 'Email, password and name are required fields'})
