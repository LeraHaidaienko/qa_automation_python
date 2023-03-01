import json
import requests
import logging
from assertpy import assert_that
import pytest

# create logger
logger = logging.getLogger('test_logger')
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.FileHandler("test.log")
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to file_handlerh
ch.setFormatter(formatter)

# add file_handlerh to logger
logger.addHandler(ch)

url_0 = "https://www.aqa.science/"
login = "admin"
pwd = "admin123"


@pytest.fixture(autouse=True, scope="module")
def change_data():
    return {}


class TestSuite:

    def test_get(self, change_data):
        # Делаем get запрос, получаем ответ
        response = requests.get(url_0)

        # Проверяем что ответ равен искомой строке
        assert response.text == '{"users":"https://www.aqa.science/users/",' \
                                '"groups":"https://www.aqa.science/groups/"}'

        # Конвертируем ответ в json структуру
        data = response.json()
        logger.info(f"json converted to internal {type(data)}")

        # Проверяем что в data у нас есть следующие ключи
        assert_that(data).contains_key("users", "groups")

        # Обновляем данные change_data данными из data
        change_data.update(data)

    def test_get_users(self, change_data):
        # Копируем сылку на users в переменную
        user_link = change_data["users"]

        # Создаем массив из ожидаемых ключей
        expected_keys = ["count", "next", "previous", "results"]

        # Делаем запрос на получение данных о пользователях, авторизируясь
        response = requests.get(user_link, auth=(login, pwd)).json()

        # Сохраняем ссылку на следующую страницу пользователей
        change_data['next_page_url'] = response["next"]

        # Проверяем что ответ содержит необходимые ключи
        assert_that(response).contains_key(*expected_keys)

    def test_get_users_2(self, change_data):
        next_url = change_data['next_page_url']
        expected_keys = ["count", "next", "previous", "results"]
        # Создаем переменную с именем искомого пользователя
        test_user_name = 'Test_user'

        # Добавляем переменную индикатор найденного пользователя
        user_exists = False

        # Запускаем цикл до того момента, пока есть следующая страница
        while next_url:
            # Делаем запрос на получение списка пользователей на странице
            response = requests.get(next_url, auth=(login, pwd)).json()

            # Сохраняем ссылку на следующую страницу
            next_url = response["next"]

            # Проверяем что ответ содержит необходимые ключи
            assert_that(response).contains_key(*expected_keys)

            # Открываем файл для записи и записываем туда список пользователей из response
            with open("result.json", "w+") as f:
                json.dump(response, f)

            # Открываем файл для чтения
            with open("result.json", 'r') as f:
                # читаем содержимое файла
                content = f.read()
                # проверяем есть ли имя пользователя в файле
                if test_user_name in content:
                    # Меняем индикатор на True
                    user_exists = True
                    # Выходим из цикла чтобы не делать лишние операции
                    break

        # Если пользователь существует, то проверить
        if user_exists:
            assert_that(response).contains_entry('Test_user')
        # Если пользователя не существует, то проверить
        else:
            assert_that(response).does_not_contain('Test_user')

    def test_post(self):
        # Создаем структуру данных для отправки на сервер
        post_data = {
            "username": "Test_user",
            "email": "test@mail.com",
            "groups": []
        }

        user_link = change_data["users"]
        expected_keys = ["url", "username", "email", "groups"]

        # Делаем post запрос на сервер и конвертируем ответ в json
        response = requests.post(user_link, post_data, auth=(login, pwd)).json()

        # Сохраняем url из ответа в переменную change_data
        created_user_url = response['url']
        change_data["created_user_url"] = created_user_url

        # Проверяем что ответ содержит необходимые ключи
        assert_that(response).contains_key(*expected_keys)
        # Проверяем что ответ содержит username с необходимым значением
        assert_that(response['username']).is_equal_to("Test_user")
        # Проверяем что ответ содержит email с необходимым значением
        assert_that(response['email']).is_equal_to("test@mail.com")

        with open("result.json", "w+") as f:
            json.dump(response, f)

    def test_delete(self):
        # Копируем ссылку на новосозданного пользователя
        user_link = change_data["created_user_url"]

        # Выполняем удаление пользователя используя его ссылку и delete
        requests.delete(user_link, auth=(login, pwd))

        # Делаем запрос на получение только что удаленного пользователя
        response = requests.get(user_link, auth=(login, pwd)).json()

        # Проверяем что сервер возвращает нам данные об отсутствии деталей
        assert_that(response.text).is_equal_to('{ "detail": "Not found."}')