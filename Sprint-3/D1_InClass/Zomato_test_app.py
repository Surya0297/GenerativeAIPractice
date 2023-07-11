import pytest
from Zomato_app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_get_menu(client):
    response = client.get('/menu')
    assert response.status_code == 200
   
def test_add_dish(client):
   
    dish_data = {
        'name': 'Test Dish',
        'price': 9.99,
        'available': 'yes',
        'stock': 10
    }

    response = client.post('/menu', json=dish_data)
    assert response.status_code == 200

def test_add_feedback(client):
   
    dish_id = 1 

    feedback_data = {
        'rating': 5,
        'comment': 'Great dish!'
    }

    response = client.post(f'/menu/{dish_id}/feedback', json=feedback_data)
    assert response.status_code == 200

def test_update_dish(client):
    
    dish_id = 1 

    response = client.put(f'/menu/{dish_id}')
    assert response.status_code == 200
  
def test_remove_dish(client):
   
    dish_id = 1 

    response = client.delete(f'/menu/{dish_id}')
    assert response.status_code == 200

def test_take_order(client):
    # Prepare test data
    order_data = {
        'customer': 'Test Customer',
        'items': [
            {
                'dish_id': 1,  # Replace with an existing dish_id from your application
                'quantity': 2
            },
            {
                'dish_id': 2,  # Replace with an existing dish_id from your application
                'quantity': 1
            }
        ]
    }

    response = client.post('/orders', json=order_data)
    assert response.status_code == 200

def test_get_orders(client):
    response = client.get('/orders')
    assert response.status_code == 200

def test_get_feedback(client):
    # Prepare test data
    dish_id = 1  # Replace with an existing dish_id from your application

    response = client.get(f'/menu/{dish_id}/feedback')
    assert response.status_code == 200

def test_get_order(client):
    # Prepare test data
    order_id = 1  # Replace with an existing order_id from your application

    response = client.get(f'/orders/{order_id}')
    assert response.status_code == 200
