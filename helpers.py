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
        print(name)
        return name

    @staticmethod
    def random_email():
        fake = Faker()
        num = str(random.randint(111, 999))
        email = f'{fake.first_name().lower()}{num}@ya.com'
        print(email)
        return email



# random_sample = RandomHelper()
# random_sample.random_email()
# random_sample.random_string(5)