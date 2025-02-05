import allure
import pytest
from conftest import new_user_parameters, disposable_user, updated_user_parameters
from constants import Constants
from routes.user_routes import UserRoutes


class TestChangeUserData:
    @allure.title('Авторизованный юзер: изменение данных')
    @allure.description('Создаем юзера, логинимся под ним, меняем данные юзера, проверяем изменение, удаляем юзера')
    def test_login_courier_possible(self, new_user_parameters, updated_user_parameters, disposable_user):
        access_token = UserRoutes().create_user_return_access_token(new_user_parameters)
        response = UserRoutes().patch_user_data(access_token, new_user_parameters['email'], new_user_parameters['name'])
        UserRoutes().delete_user(access_token)
        assert response.status_code == 200, f"Ошибка: ожидается статус ответа 200, но получили '{response.status_code}'"
        assert response.json()["success"] == True
        assert len(response.json()) == 2

    @allure.title('Неавторизованный юзер: изменение данных') #updated
    @allure.description(
        'Создаем курьера, логинимся под ним под неправильным емейлом/паролем, проверяем ошибку, удаляем курьера')
    @pytest.mark.parametrize("wrong_key", ["email", "password"])
    def test_login_courier_incorrect_parameters(self, wrong_key, new_user_parameters, disposable_user):
        access_token, new_user_parameters, response = disposable_user
        # Изменяем параметры для теста
        new_courier_parameters_wrong_key = new_user_parameters.copy()
        new_courier_parameters_wrong_key[wrong_key] = 'wrong_value'
        # Логинимся с неправильными параметрами
        response = UserRoutes().login_user(new_courier_parameters_wrong_key.get("email"),
                                          new_courier_parameters_wrong_key.get("password"))
        assert response.status_code == 401, f"Ошибка: ожидается статус ответа 404, но получили '{response.status_code}'"
        assert response.json()["message"] == Constants.USER_WRONG_KEY_MSG