import pytest
from main import create_app

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Home Page" in response.data  # Adjust to match your content

def test_login_page(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert b"Login" in response.data