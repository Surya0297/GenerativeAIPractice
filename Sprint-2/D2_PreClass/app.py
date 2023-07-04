from flask import Flask, request, jsonify
import pickle
from flask_cors import CORS  # Import the CORS module



app = Flask(__name__)
CORS(app) 
stocks = {}
orders = {}


@app.route('/menu', methods=['GET'])
def get_menu():
    return jsonify(stocks)

@app.route('/menu', methods=['POST'])
def add_dish():
    print("1")
    dish = request.json
    print(dish)
    if 'name' in dish and 'price' in dish and 'available' in dish and 'stock' in dish:
        if len(stocks) > 0:
            last_key = max(stocks.keys())
        else:
            last_key = 0

        dish_id = last_key + 1
        stocks[dish_id] = dish
        saveMenu()
        return jsonify({'message': 'Dish added successfully'})
    else:
        return jsonify({'error': 'Invalid dish data'})

@app.route('/menu/<int:dish_id>', methods=['PUT'])
def update_dish(dish_id):
    if dish_id in stocks:
        dish = stocks[dish_id]
        if dish['available'] == 'yes':
            dish['available'] = 'no'
        else:
            dish['available'] = 'yes'
        saveMenu()
        return jsonify({'message': 'Dish availability updated'})
    else:
        return jsonify({'error': 'Dish not found'})

@app.route('/menu/<int:dish_id>', methods=['DELETE'])
def remove_dish(dish_id):
    if dish_id in stocks:
        del stocks[dish_id]
        saveMenu()
        return jsonify({'message': 'Dish deleted successfully'})
    else:
        return jsonify({'error': 'Dish not found'})

@app.route('/orders', methods=['POST'])
def take_order():
    order = request.json
    if 'customer' in order and 'items' in order:
        order_list = []
        for item in order['items']:
            dish_id = item['dish_id']
            quantity = item['quantity']
            if dish_id in stocks:
                dish = stocks[dish_id]
                if dish['available'] == 'yes' and quantity <=int( dish['stock']):
                    Q=int(dish['stock'])
                    Q-= quantity
                    dish['stock']=Q
                    order_list.append({'dish': dish['name'], 'quantity': quantity})
                    if dish['stock'] == 0:
                        dish['available'] = 'no'
                else:
                    return jsonify({'error': f"{dish['name']} cannot be added as it is out of stock"})
            else:
                return jsonify({'error': f"Dish with id {dish_id} does not exist"})

        if len(orders) == 0:
            order_id = 1
        else:
            order_id = max(orders.keys()) + 1

        orders[order_id] = {'customer': order['customer'], 'order': order_list, 'status': 'received'}
        saveOrder()
        saveMenu()
        return jsonify({'message': 'Order successful'})
    else:
        return jsonify({'error': 'Invalid order data'})


@app.route('/orders', methods=['GET'])
def get_orders():
    return jsonify(orders)

@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = orders.get(order_id)
    if order:
        return jsonify(order)
    return 'Order not found', 404

@app.route('/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    order = orders.get(order_id)
    if order:
        status = request.json.get('status')
        if status:
            order['status'] = status
            return 'Order status updated successfully'
        return 'No status provided', 400
    return 'Order not found', 404

# Define other routes for viewing stock, viewing orders, etc.

def saveMenu():
    with open("menu.pkl", "wb") as file:
        pickle.dump(stocks, file)
    print("Menu updated.")

def loadMenu():
    try:
        with open("menu.pkl", "rb") as file:
            stocks.update(pickle.load(file))
        print("Menu data loaded from file.")
    except FileNotFoundError:
        print("Menu data file not found. Starting with an empty menu.")

def saveOrder():
    with open("order.pkl", "wb") as file:
        pickle.dump(orders, file)
    print("Order data saved to file.")

def loadOrders():
    try:
        with open("order.pkl", "rb") as file:
            orders.update(pickle.load(file))
        print("Order data loaded from file.")
    except FileNotFoundError:
        print("Order data file not found. Starting with an empty order list.")

def load_data():
    loadMenu()
    loadOrders()

if __name__ == '__main__':
    load_data()
    app.run()
