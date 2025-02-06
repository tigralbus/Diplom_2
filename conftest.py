import pytest
from helpers import RandomHelper
from routes.order_routes import OrderRoutes
from routes.user_routes import UserRoutes


@pytest.fixture(scope='function')
def new_user_parameters():
    # генерируем имя, емейл, пароль
    email = RandomHelper.random_email()
    password = RandomHelper.random_string(6)
    name = RandomHelper.random_name()

    # собираем тело запроса
    parameters = {
        "email": email,
        "password": password,
        "name": name
    }
    print(password)
    return parameters


@pytest.fixture(scope='function')
def updated_user_parameters(new_user_parameters):
    parameters_updated = {"name": f"{new_user_parameters["name"]}_updated",
                          "email": f"{new_user_parameters["email"]}_updated"}
    return parameters_updated


@pytest.fixture(scope='function')
def disposable_user(new_user_parameters):
    user = UserRoutes()
    # Регистрируем нового юзера и получаем его access_token
    response = user.create_user(new_user_parameters)
    access_token = response.json()['accessToken']
    yield access_token, new_user_parameters, response  # Передаем access_token и параметры ответа в тест
    # Выполняем удаление юзера после завершения теста
    user.delete_user(access_token)


@pytest.fixture(scope='function')
def disposable_order(new_user_parameters):
    user = UserRoutes()
    # Регистрируем нового юзера и получаем его access_token
    access_token = user.create_user(new_user_parameters).json()['accessToken']
    # Получить список ингредиентов
    order = OrderRoutes()
    ingredients_ids_list = order.get_ingredients_list()
    response = order.create_order(access_token, ingredients_ids_list, 3, 5)
    yield access_token, new_user_parameters, ingredients_ids_list, response  # Передаем access_token и параметры ответа в тест
    # Выполняем удаление юзера после завершения теста
    user.delete_user(access_token)
