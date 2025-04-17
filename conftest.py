import pytest
import allure
import requests
from urls import *
from data import *

@pytest.fixture
@allure.title('Фикстура создает пользователя с рандомными кредами и удаляет его из базы после прохождения теста')
def create_new_user_and_delete():
    payload_cred = {
        'email' : create_random_email(),
        'password' : create_random_password(),
        'name' : create_random_username()
    }
    response = requests.post(Urls.user_register, data=payload_cred)
    response_body = response.json()

    yield payload_cred, response_body

    access_token = response_body['accessToken']
    requests.delete(Urls.user_delete, headers={'Authorization': access_token})

@pytest.fixture
@allure.title('Фикстура создает пользователя и заказ на его аккаунт')
def create_user_and_order_and_delete(create_new_user_and_delete):
    access_token = create_new_user_and_delete[1]['accessToken']
    headers = {'Authorization': access_token}
    payload = {'ingredients': [IngredientData.burger_2]}
    response_body = requests.post(Urls.receive_user_orders, data=payload, headers=headers)

    yield access_token, response_body

    requests.delete(Urls.user_delete, headers={'Authorization': access_token})