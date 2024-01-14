from flask import Flask, request
import requests


app = Flask(__name__)


# Регистрация
# Получение логина-пароля
# Проверка на уникальность логина -> db_service (/user/<login>)
# Сохранение логина-пароля в базу данных
@app.post("/sign_in")
def sign_in():
    login = request.json.get("login")
    password = request.json.get("password")
    response = requests.get(f"http://{4}:{4}/user/{login}") # запрос на db_service
    if response.json().is_exist is True:
        return {"is_exist": True}, 400
    # запрос на db_service на создание пользователя


# Авторизация


# Сменить пароль (PUT)

# Удалить аккаунт (DELETE)

