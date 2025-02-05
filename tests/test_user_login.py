import allure
import pytest
from conftest import new_user_parameters, disposable_user
from constants import Constants
from routes.user_routes import UserRoutes


class TestLoginUser:
    @allure.title('Логин юзера')
    @allure.description('Создаем юзера, логинимся под ним, проверяем логин, удаляем юзера')
    def test_login_user_possible(self, new_user_parameters, disposable_user):
        access_token, new_user_parameters, response = disposable_user
        response_login = UserRoutes().login_user(new_user_parameters['email'], new_user_parameters['password'])
        assert response_login.status_code == 200, f"Ошибка: ожидается статус ответа 200, но получили '{response_login.status_code}'"
        assert response_login.json()["success"] == True
        assert len(response.json()) == 4

    @allure.title('Логин юзера с неверным емейлом/паролем') #updated
    @allure.description(
        'Создаем юзера, логинимся под ним под неправильным емейлом/паролем, проверяем ошибку, удаляем юзера')
    @pytest.mark.parametrize("wrong_key", ["email", "password"])
    def test_login_user_incorrect_parameters_impossible(self, wrong_key, new_user_parameters, disposable_user):
        access_token, new_user_parameters, response = disposable_user
        # Изменяем параметры для теста
        new_courier_parameters_wrong_key = new_user_parameters.copy()
        new_courier_parameters_wrong_key[wrong_key] = 'wrong_value'
        # Логинимся с неправильными параметрами
        response = UserRoutes().login_user(new_courier_parameters_wrong_key.get("email"),
                                          new_courier_parameters_wrong_key.get("password"))
        assert response.status_code == 401, f"Ошибка: ожидается статус ответа 404, но получили '{response.status_code}'"
        assert response.json()["message"] == Constants.USER_WRONG_KEY_MSG