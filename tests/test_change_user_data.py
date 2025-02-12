import allure
from conftest import new_user_parameters, updated_user_parameters
from constants import Constants
from routes.user_routes import UserRoutes


class TestChangeUserData:
    @allure.title('Авторизованный юзер изменение данных')
    @allure.description('Создаем юзера, меняем данные юзера, проверяем изменение, удаляем юзера')
    def test_change_user_data_possible(self, new_user_parameters, request):
        access_token = UserRoutes().create_user_return_access_token(new_user_parameters)
        updated_user_parameters = request.getfixturevalue(
            "updated_user_parameters")  # принудительный вызов фикстуры только после создания пользователя чтобы параметры менялись после запуска теста
        response = UserRoutes().patch_user_data(access_token, updated_user_parameters['name'],
                                                updated_user_parameters['email'])
        UserRoutes().delete_user(access_token)
        assert response.status_code == 200, f"Ошибка: ожидается статус ответа 200, но получили '{response.status_code}'"
        assert response.json()["success"] == True
        assert response.json()["user"]["email"] == updated_user_parameters['email'] and response.json()["user"][
            "name"] == updated_user_parameters['name']

    @allure.title('Неавторизованный юзер: изменение данных')  # updated
    @allure.description(
        'Не авторизуемся, меняем данные юзера, проверяем ответ')
    def test_login_courier_incorrect_parameters(self, updated_user_parameters):
        response = UserRoutes().patch_user_data('', updated_user_parameters['name'],
                                                updated_user_parameters['email'])
        assert response.status_code == 401, f"Ошибка: ожидается статус ответа 404, но получили '{response.status_code}'"
        assert response.json()["success"] == False
        assert response.json()["message"] == Constants.USER_NOT_AUTHORIZED
