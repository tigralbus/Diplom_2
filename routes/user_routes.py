import allure
import requests
from constants import Constants


class UserRoutes:
    @allure.step('Создать юзера')
    def create_user(self, new_user_parameters):
        response = requests.post(f"{Constants.URL}/auth/register", data=new_user_parameters)
        return response

    @allure.step('Создать юзера для получения accessToken')
    def create_user_return_access_token(self, new_user_parameters):
        response = requests.post(f"{Constants.URL}/auth/register", data=new_user_parameters)
        return response.json()['accessToken']

    @allure.step('Логин юзера')
    def login_user(self, email, password):
        login_payload = {
            "email": email,
            "password": password,
        }
        response_login = requests.post(f"{Constants.URL}/auth/login",
                                       data=login_payload)
        return response_login

    @allure.step('Логин юзера для получения accessToken')
    def login_user_return_access_token(self, email, password):
        login_payload = {
            "email": email,
            "password": password,
        }
        response_login = requests.post(f"{Constants.URL}/auth/login", data=login_payload)
        return response_login.json()['accessToken']

    @allure.step('Изменить данные юзера')
    def patch_user_data(self, access_token, name, email):
        headers = {
            "Authorization": f"{access_token}"
        }
        data_load = {
            "name": name,
            "email": email,
        }
        response = requests.patch(f"{Constants.URL}/auth/user", data=data_load, headers=headers)
        return response

    @allure.step('Удалить юзера')
    def delete_user(self, access_token):
        headers = {
            "Authorization": f"{access_token}"
        }
        response_delete = requests.delete(f"{Constants.URL}/auth/user", headers=headers)
        return response_delete
