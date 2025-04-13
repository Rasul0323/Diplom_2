from conftest import *

class TestCreatingAnOrder:
    @allure.title('Проверка ответа при создании заказа с указанными ингредиентами для аутентифицированного пользователя')
    @allure.description(' Выполняем два теста с разными наборами ингредиентов в бургере.'
                        'Аккаунт создается фикстурой перед тестом и после него удаляется из базы данных')
    @pytest.mark.parametrize('burger_ingredients', [IngredientData.burger_1, IngredientData.burger_2])
    def test_creating_an_order_ingredients_authorization_success(self, create_new_user_and_delete, burger_ingredients):
        headers = {'Authorization': create_new_user_and_delete[1]['accessToken']}
        payload = {'ingredients': [burger_ingredients]}
        response = requests.post(Urls.receiving_orders, data=payload, headers=headers)
        deserials = response.json()
        assert response.status_code == 200
        assert deserials['success'] is True
        assert 'name' in deserials.keys()
        assert 'number' in deserials['order'].keys()

    @allure.title('Проверка ответа при создании заказа с указанными ингредиентами для неавторизованного пользователя')
    @allure.description('Выполняем два теста с разными наборами ингредиентов в бургере.'
                        'Токен аккаунта не передается.')
    @pytest.mark.parametrize('burger_ingredients', [IngredientData.burger_1, IngredientData.burger_2])
    def test_creating_an_order_ingredients_not_authorized_error(self, burger_ingredients):
        payload = {'ingredients': [burger_ingredients]}
        response = requests.post(Urls.receiving_orders, data=payload, headers=Urls.headers)
        assert {response.status_code == 401 and response.json() == 'success': False,
                'message': 'You should be authorised'}

    @allure.title('Проверка ответа при создании заказа без ингредиентов для авторизованного пользователя')
    @allure.description('Хеш ингредиента не передается в запросе. Аккаунт пользователя создается в фикстуре перед тестом.'
                        'После теста аккаунт удаляется.')
    def test_creating_an_order_no_ingredients_authorization_error(self, create_new_user_and_delete):
        headers = {'Authorization': create_new_user_and_delete[1]['accessToken']}
        payload = {'ingredients': []}
        response = requests.post(Urls.receiving_orders, data=payload, headers=headers)
        assert response.status_code == 400 and response.json() == {'success': False, 'message': 'Ingredient ids must be provided'}

    @allure.title('Проверка ответа при создании заказа без ингредиентов для неавторизованного пользователя')
    @allure.description('Хеш ингредиента не передается в запросе. Токен аккаунта не передается в запросе.')
    def test_creating_an_order_no_ingredients_not_authorized_error(self):
        payload = {'ingredients': []}
        response = requests.post(Urls.receiving_orders, data=payload, headers=Urls.headers)
        assert response.status_code == 400 and response.json() == {'success': False, 'message': 'Ingredient ids must be provided'}

    @allure.title('Проверка ответа при создании заказа с указанием неверного хеша ингредиента для авторизованного пользователя')
    @allure.description('Передан неверный хеш ингредиента. Аккаунт пользователя создается в фикстуре перед тестом.'
                        'После теста аккаунт удаляется.')
    def test_creating_an_order_invalid_hash_authorization_error(self, create_new_user_and_delete):
        headers = {'Authorization': create_new_user_and_delete[1]['accessToken']}
        payload = {'ingredients': [IngredientData.invalid_hash_ingredient]}
        response = requests.post(Urls.receiving_orders, data=payload, headers=headers)
        assert response.status_code == 400 and response.json() == {'success': False, 'message': 'One or more ids provided are incorrect'}
