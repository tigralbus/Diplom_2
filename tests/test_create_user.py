import allure
import pytest
from conftest import new_user_parameters, disposable_user
from constants import Constants
from routes.user_routes import UserRoutes


class TestCreateUser:
    @allure.title('Регистрация юзера')
    @allure.description('Создаем юзера, проверяем создание юзера, удаляем юзера')
    def test_create_user_possible(self, new_user_parameters, disposable_user):
        access_token, new_user_parameters, response = disposable_user  # Получаем access_token юзера и параметра из фикстуры
        assert response.status_code == 200, f"Ошибка: ожидается статус ответа 200, но получили '{response.status_code}'"
        assert response.json()['success'] == True
        assert len(response.json()) == 4

    @allure.title('Регистрация уже существующего юзера')
    @allure.description(
        'Создаем юзера, создаем повторно юзера с теми же параметрами, удаляем юзера, проверяем сообщение об ошибке')
    def test_create_existing_user_impossible(self, new_user_parameters):
        access_token = UserRoutes().create_user_return_access_token(new_user_parameters)
        response = UserRoutes().create_user(new_user_parameters)
        UserRoutes().delete_user(access_token)
        assert response.status_code == 403, f"Ошибка: ожидается статус ответа 403, но получили '{response.status_code}'"
        assert response.json()['success'] == False
        assert response.json()['message'] == Constants.USER_EXISTS_MSG

    @allure.title('Регистрация юзера без обязательного поля')
    @allure.description('Создаем юзера требуемого без поля, проверяем сообщение об ошибке')
    @pytest.mark.parametrize("missing_key", ["name", "password", "email"])
    def test_create_user_without_required_data_impossible(self, new_user_parameters, missing_key):
        user_parameters_missing_key = {k: v for k, v in new_user_parameters.items() if
                                       k != missing_key}  # копируем отфильтрованный словарь через генератор словаря
        response = UserRoutes().create_user(user_parameters_missing_key)
        assert response.status_code == 403, f"Ошибка: ожидается статус ответа 403, но получили '{response.status_code}'"
        assert response.json()['success'] == False
        assert response.json()['message'] == Constants.USER_REQUIRED_FIELDS_MSG
