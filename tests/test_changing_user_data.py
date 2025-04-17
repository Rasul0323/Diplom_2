from conftest import *

class TestChangingUserData:
    user_update_data = {
        'email': create_random_email(),
        'password': create_random_password(),
        'name': create_random_username()
    }

    @allure.title('Проверка ответа на запрос изменения данных пользователя при авторизации этого пользователя')
    def test_changing_user_data_authenticated_user_success(self, create_new_user_and_delete):
        response = requests.patch(Urls.user_update, headers={
            'Authorization': create_new_user_and_delete[1]['accessToken']}, data=TestChangingUserData.user_update_data)
        deserials = response.json()
        assert response.status_code == 200
        assert deserials['success'] is True
        assert deserials['user']['email'] == TestChangingUserData.user_update_data['email']
        assert deserials['user']['name'] == TestChangingUserData.user_update_data['name']

    @allure.title('Проверка ответа на запрос изменения данных пользователя когда он не авторизован')
    def test_changing_user_data_an_unidentified_user_error(self):
        response = requests.patch(Urls.user_update, headers=Urls.headers, data=TestChangingUserData.user_update_data)
        assert {response.status_code == 401 and response.json() == 'success': False, 'message': 'You should be authorised'}
