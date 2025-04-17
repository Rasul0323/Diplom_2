from conftest import *

class TestLoginUser:

    @allure.title('Проверка успешной аутентификации пользователя при передаче учетных данных существующего пользователя')
    @allure.description('Аутентификация происходит с помощью фикстуры которая создает аккаунт для проверки.'
                        'После теста аккаунт удаляется. В ответе проверяются код и тело, получение accessToken и refreshToken')
    def test_login_user_sign_in_with_an_existing_account_success(self, create_new_user_and_delete):
        payload = create_new_user_and_delete[0]
        response = requests.post(Urls.user_auth, data=payload)
        deserials = response.json()
        assert response.status_code == 200
        assert deserials['success'] is True
        assert 'accessToken' in deserials.keys()
        assert 'refreshToken' in deserials.keys()
        assert deserials['user']['email'] == create_new_user_and_delete[0]['email']
        assert deserials['user']['name'] == create_new_user_and_delete[0]['name']

    @allure.title('Проверка ответа на запрос при аутентификации существующего пользователя при передаче неверного email')
    def test_login_user_incorrect_email_error(self):
        payload = {
            'email': create_random_email(),
            'password': UsersData.password,
        }
        response = requests.post(Urls.user_auth, data=payload)
        assert response.status_code == 401 and response.json() == {'success': False, 'message': 'email or password are incorrect'}

    @allure.title('Проверка ответа на запрос при аутентификации существующего пользователя при передаче неверного пароля')
    def test_login_user_incorrect_password_error(self):
        payload = {
            'email': UsersData.email,
            'password': create_random_password(),
        }
        response = requests.post(Urls.user_auth, data=payload)
        assert response.status_code == 401 and response.json() == {'success': False, 'message': 'email or password are incorrect'}

