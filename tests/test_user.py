from fastapi.testclient import TestClient
import pytest

from src.main import app

client = TestClient(app)

users = [
    {
        'id': 1,
        'name': 'Ivan Ivanov',
        'email': 'i.i.ivanov@mail.com',
    },
    {
        'id': 2,
        'name': 'Petr Petrov',
        'email': 'p.p.petrov@mail.com',
    }
]

def test_get_existed_user():
    """Получение существующего пользователя"""
    response = client.get("/api/v1/user", params={'email': users[0]['email']})
    assert response.status_code == 200
    assert response.json() == users[0]

def test_get_unexisted_user():
    """Получение несуществующего пользователя"""
    response = client.get("/api/v1/user", params={'email': 'noone@nowhere.xyz'})
    assert response.status_code == 404
    assert response.json() == {'detail': 'User not found'}

def test_create_user_with_valid_email():
    """Создание пользователя с уникальной почтой"""
    new_user = {'name': 'Anna Sidorova', 'email': 'a.sidorova@mail.com'}
    response = client.post("/api/v1/user", json=new_user)
    assert response.status_code == 201
    new_id = response.json()
    assert isinstance(new_id, int) and new_id > 0

    resp2 = client.get("/api/v1/user", params={'email': new_user['email']})
    assert resp2.status_code == 200
    assert resp2.json() == {'id': new_id, **new_user}

def test_create_user_with_invalid_email():
    """Создание пользователя с почтой, которую уже используют"""
    dup = {'name': 'Duplicate', 'email': users[0]['email']}
    response = client.post("/api/v1/user", json=dup)
    assert response.status_code == 409
    assert response.json() == {'detail': 'User with this email already exists'}

def test_delete_user():
    """Удаление пользователя"""
    email = users[1]['email']
    del_resp = client.delete("/api/v1/user", params={'email': email})
    assert del_resp.status_code == 204

    resp = client.get("/api/v1/user", params={'email': email})
    assert resp.status_code == 404
    assert resp.json() == {'detail': 'User not found'}
