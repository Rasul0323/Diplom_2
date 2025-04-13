from conftest import *
import requests

class TestReceivingUserOrders:

    @allure.title('Проверка ответа о успешном получении списка заказов для аутентифицированного пользователя')
    @allure.description('Аккаунт и заказ создаются фикстурой перед тестом, тест получает список c заказом, после этого аккаунт удаляется из базы данных')
    def test_receiving_user_orders_authorization_success(self, create_user_and_order_and_delete):
        headers = {'Authorization': create_user_and_order_and_delete[0]}
        response = requests.get(Urls.receive_user_orders, headers=headers)
        deserials = response.json()
        assert response.status_code == 200
        assert deserials['success'] is True
        assert 'orders' in deserials.keys()
        assert 'total' in deserials.keys()

    @allure.title('Проверка ответа при получении списка заказов для неаутентифицированного пользователя')
    def test_receiving_user_orders_not_authorized_error(self):
        response = requests.get(Urls.receive_user_orders, headers=Urls.headers)
        assert response.status_code == 401 and response.json() == {'success': False, 'message': 'You should be authorised'}

