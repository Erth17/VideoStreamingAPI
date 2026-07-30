import pytest
from App import app, users, payments

@pytest.fixture
def client():
    app.config['TESTING'] = True

    users.clear()
    payments.clear()

    with app.test_client() as client:
        yield client

def valid_user(card=True):
    user = {
        "username" : "TestUser1",
        "password" : "Password1",
        "email" : "test@pytest.com",
        "DoB" : "2000-01-01"
    }

    if card:
        user["card_number"] = "1234567887654321"

    return user

def test_register_user_success(client):
    response = client.post("/users", json=valid_user())

    assert response.status_code == 201
    assert len(users) == 1

def test_register_user_validation(client):
    invalid = valid_user()
    invalid["password"] = "invalidpassword"

    response = client.post("/users", json=invalid)

    assert response.status_code == 400

def test_user_under_18_status_403(client):
    user = valid_user()
    user["DoB"] = "2020-01-01"

    response = client.post("/users", json=user)

    assert response.status_code == 403

def test_get_users_filter_credit_card(client):
    client.post("/users", json=valid_user(card=True))

    second_user = valid_user(card=False)
    second_user["username"] = "TestUser2"

    client.post("/users", json=second_user)

    yes_response = client.get("/users?CreditCard=Yes")
    no_response = client.get("/users?CreditCard=No")

    assert len(yes_response.get_json()) == 1
    assert len(no_response.get_json()) == 1

def test_payment_success(client):
    client.post("/users", json=valid_user())

    payment = {
        "card_number" : "1234567887654321",
        "amount" : "100",
    }

    reponse = client.post("/payments", json=payment)

    assert reponse.status_code == 201
    assert len(payments) == 1

def test_payment_validation(client):
    payment = {
        "card_number" : "1111",
        "amount" : "1000",
    }

    response = client.post("/payments", json=payment)

    assert response.status_code == 400

def test_payment_not_found(client):
    payment = {
        "card_number" : "1234567812345678",
        "amount" : "999",
    }

    response = client.post("/payments", json=payment)

    assert response.status_code == 404