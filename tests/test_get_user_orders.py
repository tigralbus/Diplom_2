import allure
from conftest import new_user_parameters
from constants import Constants
from routes.order_routes import OrderRoutes
from routes.user_routes import UserRoutes


class TestCreateUser:
    @allure.title('Получение списка заказов авторизованного юзера')
    @allure.description(
        'Создаем юзера, получаем список ингредиентов, создаем 2 заказа юзеру, получаем список заказов, проверяем, удаляем юзера')
    def test_get_orders_list_for_user_possible(self, new_user_parameters):
        access_token = UserRoutes().create_user_return_access_token(new_user_parameters)
        ingredients_ids_list = OrderRoutes().get_ingredients_list()
        OrderRoutes().create_order(access_token, ingredients_ids_list, 5, 6)
        OrderRoutes().create_order(access_token, ingredients_ids_list, 1, 2)
        response = OrderRoutes().get_orders_for_user(access_token)
        UserRoutes().delete_user(access_token)

        assert response.status_code == 200, f"Ошибка: ожидается статус ответа 200, но получили '{response.status_code}'"
        assert response.json()['success'] == True
        assert len(response.json()["orders"]) == 2

    @allure.title('Получение списка заказов без авторизации')
    @allure.description(
        'Создаем юзера, получаем список ингредиентов, создаем 2 заказа юзеру, получаем список заказов, проверяем, удаляем юзера')
    def test_get_orders_list_without_auth_impossible(self, new_user_parameters):
        response = OrderRoutes().get_orders_for_user('')

        assert response.status_code == 401, f"Ошибка: ожидается статус ответа 401, но получили '{response.status_code}'"
        assert response.json()['success'] == False
        assert response.json()['message'] == Constants.USER_NOT_AUTHORIZED
