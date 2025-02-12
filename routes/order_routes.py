import allure
import requests
from constants import Constants


class OrderRoutes:
    @allure.step('Создать заказ с 2 ингредиентами по индексу')
    def create_order(self, access_token, ingredients_ids_list, index1, index2):
        ingredients_load = {
            "ingredients": [ingredients_ids_list[index1], ingredients_ids_list[index2]]
        }
        headers = {
            "Authorization": f"{access_token}"
        }
        response = requests.post(f"{Constants.URL}/orders", data=ingredients_load, headers=headers)
        return response

    @allure.step('Создать заказ со всеми ингредиентами из списка')
    def create_order_all_ingredients(self, access_token, ingredients_ids_list):
        ingredients_load = {
            "ingredients": ingredients_ids_list
        }
        headers = {
            "Authorization": f"{access_token}"
        }
        response = requests.post(f"{Constants.URL}/orders", data=ingredients_load, headers=headers)
        return response

    @allure.step('Получить список ингредиентов')
    def get_ingredients_list(self):
        response = requests.get(f"{Constants.URL}/ingredients")
        ingredients_ids_list = []
        for i in range(len(response.json()["data"])):
            ingredients_ids_list.append(response.json()["data"][i]["_id"])
        return ingredients_ids_list

    @allure.step('Получить список заказов пользователя')
    def get_orders_for_user(self, access_token):
        headers = {
            "Authorization": f"{access_token}"
        }
        response = requests.get(f"{Constants.URL}/orders", headers=headers)
        return response
