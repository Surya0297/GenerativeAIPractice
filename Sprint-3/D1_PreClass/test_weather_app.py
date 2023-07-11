import json
from flask import Flask
from flask.testing import FlaskClient
import pytest
from weather_app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client

def test_get_weather_info(client: FlaskClient):
    response = client.get('/weather/San Francisco')
    assert response.status_code == 200

    data = json.loads(response.data)
    assert data == {'temperature': 14, 'weather': 'Cloudy'}

def test_add_weather_info(client: FlaskClient):
    data = {
        'city': 'Chicago',
        'temperature': 18,
        'weather': 'Cloudy',
    }
    response = client.post('/weather', json=data)
    assert response.status_code == 201

    response_data = json.loads(response.data)
    assert response_data == {'message': 'Weather data added successfully'}

def test_update_weather_info(client: FlaskClient):
    data = {
        'temperature': 22,
        'weather': 'Sunny',
    }
    response = client.put('/weather/Seattle', json=data)
    assert response.status_code == 200

    response_data = json.loads(response.data)
    assert response_data == {'message': 'Weather data updated successfully'}

def test_delete_weather_info(client: FlaskClient):
    response = client.delete('/weather/Austin')
    assert response.status_code == 200

    response_data = json.loads(response.data)
    assert response_data == {'message': 'Weather data deleted successfully'}
