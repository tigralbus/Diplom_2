import allure
from conftest import new_user_parameters, disposable_order
from constants import Constants
from routes.order_routes import OrderRoutes
from routes.user_routes import UserRoutes


class TestCreateUser:
    @allure.title('Создание заказа с авторизацией')
    @allure.description('Создаем юзера, получаем список ингредиентов, создаем заказ, проверяем, удаляем юзера')
    def test_create_order_for_authorized_user_possible(self, new_user_parameters, disposable_order):
        access_token, new_user_parameters, ingredients_ids_list, response = disposable_order

        assert response.status_code == 200, f"Ошибка: ожидается статус ответа 200, но получили '{response.status_code}'"
        assert response.json()['success'] == True
        assert len(response.json()["order"]["ingredients"]) == 2

    @allure.title('Создание заказа без авторизации')
    @allure.description('Создаем заказ без авторизации, проверяем')
    def test_create_order_without_authorization_impossible(self):
        ingredients_ids_list = OrderRoutes().get_ingredients_list()
        response = OrderRoutes().create_order_all_ingredients('', ingredients_ids_list)

        assert response.status_code == 200, f"Ошибка: ожидается статус ответа 200, но получили '{response.status_code}'"
        assert response.json()['success'] == True
        assert len(response.json()["order"]) == 1

    @allure.title('Создание заказа без ингредиентов')
    @allure.description('Создаем юзера, создаем заказ без ингредиентов, проверяем, удаляем юзера')
    def test_create_order_without_ingredients_impossible(self, new_user_parameters):
        access_token = UserRoutes().create_user_return_access_token(new_user_parameters)
        ingredients_ids_list = []
        response = OrderRoutes().create_order_all_ingredients(access_token, ingredients_ids_list)
        UserRoutes().delete_user(access_token)

        assert response.status_code == 400, f"Ошибка: ожидается статус ответа 400, но получили '{response.status_code}'"
        assert response.json()['success'] == False
        assert response.json()['message'] == Constants.NO_INGREDIENTS_MSG

    @allure.title('Создание заказа с некорректным хешем ингредиента')
    @allure.description('Создаем юзера, создаем заказ с некорректным хешем ингредиента, проверяем, удаляем юзера')
    def test_create_order_wit_incorrect_ingredient_impossible(self, new_user_parameters):
        access_token = UserRoutes().create_user_return_access_token(new_user_parameters)
        ingredients_ids_list = ["661c0c5a71d1f82001bdaaa6dnot111real11hash"]
        response = OrderRoutes().create_order_all_ingredients(access_token, ingredients_ids_list)
        UserRoutes().delete_user(access_token)

        assert response.status_code == 500, f"Ошибка: ожидается статус ответа 500, но получили '{response.status_code}'"
