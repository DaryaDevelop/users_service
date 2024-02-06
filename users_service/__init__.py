import os
import requests

from flask import Flask, request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


# Регистрация
# Получение логина-пароля
# Проверка на уникальность логина -> db_service (/user/<login>)
# Сохранение логина-пароля в базу данных
# запрос на db_service на создание пользователя
@app.post("/sign_up")
def sign_up():
    login = request.json.get("login")
    password = request.json.get("password")
    if not login or not password:
        return {
            "status": 1,
            "description": "No such data in request",
            "data": {}
        }, 400
    response = requests.get(f"http://{os.getenv('DB_SERVICE_HOST')}:{os.getenv('DB_SERVICE_PORT')}/user/{login}") # запрос на db_service
    if response.status_code >= 400:
        return {
            "status": 2,
            "description": "User already exist",
            "data": {}
        }, 400
    response = requests.post(f"http://{os.getenv('DB_SERVICE_HOST')}:{os.getenv('DB_SERVICE_PORT')}/user",
                             json=request.json,
                             headers={"Contant-Type": "application/json"})
    return {
        "status": response.json()["status"],
        "description": response.json()["description"],
        "data": response.json()["data"]
    }, response.status_code

# Авторизация
@app.post("/sign_in")
def sign_in():
    login = request.json.get("login")
    password = request.json.get("password")
    if not login or not password:
        return {
            "status": 1,
            "description": "No such data in request",
            "data": {}
        }, 400
    response = requests.post(f"http://{os.getenv('DB_SERVICE_HOST')}:{os.getenv('DB_SERVICE_PORT')}/sign_in",
                             json=request.json,
                             headers={"Contant-Type": "application/json"})
    return {
        "status": response.json()["status"],
        "description": response.json()["description"],
        "data": response.json()["data"]
    }, response.status_code

# Смена пароля
@app.put("/change_password")
def change_password():
    login = request.json.get("login")
    password = request.json.get("password")
    password_new = request.json.get("password_new")
    password_new_repeat = request.json.get("password_new_repeat")
    if not login or not password or not password_new or not password_new_repeat:
        return {
            "status": 1,
            "description": "No such data in request",
            "data": {}
        }, 400
    if password_new != password_new_repeat:
        return {
            "status": 5,
            "description": "Passwords do not match",
            "data": {}
        }, 400
    response = requests.put(f"http://{os.getenv('DB_SERVICE_HOST')}:{os.getenv('DB_SERVICE_PORT')}/change_password/{login}",
                           json=request.json,
                           headers={"Content-Type": "application/json"})
    return {
        "status": response.json()["status"],
        "description": response.json()["description"],
        "data": response.json()["data"]
    }, response.status_code

# Удалить аккаунт (DELETE)
@app.delete("/delete_user/<int:id>")
def delete_user(id):
    response = requests.delete(f"http://{os.getenv('DB_SERVICE_HOST')}:{os.getenv('DB_SERVICE_PORT')}/delete_user/{id}")
    return {
        "status": response.json()["status"],
        "description": response.json()["description"],
        "data": response.json()["data"]
    }, response.status_code
