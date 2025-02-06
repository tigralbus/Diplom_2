import random
import string
from faker import Faker


class RandomHelper:

    # метод генерирует строку, состоящую только из букв нижнего регистра, в качестве параметра передаём длину строки
    @staticmethod
    def random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

    @staticmethod
    def random_name():
        fake = Faker()
        fake_name = fake.first_name()
        random_string = RandomHelper().random_string(5)
        name = f'{fake_name}_{random_string}'
        return name

    @staticmethod
    def random_email():
        fake = Faker()
        num = f'{str(random.randint(11111, 999999))}'
        email = f'{fake.first_name().lower()}{num}@kilpyavr.com'
        return email
