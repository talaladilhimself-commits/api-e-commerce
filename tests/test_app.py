from flask import Flask
import pytest
from Frontend.frontend import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_homepage(client):
    """test the homepage."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"A Website where you can buy notes" in response.data

def test_register_page(client):
    """test the register page."""
    response = client.get("/register")
    assert response.status_code == 200
