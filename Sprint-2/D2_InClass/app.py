from flask import Flask, request, jsonify, render_template
import pickle
import mysql.connector
from flask_socketio import SocketIO,emit
from flask_cors import CORS  # Import the CORS module



app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='http://127.0.0.1:5500')

CORS(app, origins='http://127.0.0.1:5500')



# MySQL Configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'resdb'
}

stocks = {}
orders = {}

# Establish MySQL connection
def connect():
    return mysql.connector.connect(**db_config)

# Create stocks table
def create_stocks_table():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stocks (
            id INT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            price DECIMAL(10, 2) NOT NULL,
            available ENUM('yes', 'no') NOT NULL,
            stock INT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# Create orders table
def create_orders_table():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INT PRIMARY KEY,
            customer VARCHAR(255) NOT NULL,
            status VARCHAR(255) NOT NULL
        )
    """)

    conn.commit()
    conn.close()

# Create feedback table
def create_feedback_table():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INT PRIMARY KEY AUTO_INCREMENT,
            dish_id INT,
            rating INT NOT NULL,
            comment VARCHAR(255),
            FOREIGN KEY (dish_id) REFERENCES stocks(id)
        )
    """)

    conn.commit()
    conn.close()

@app.route('/menu', methods=['GET'])
def get_menu():
    return jsonify(stocks)

@app.route('/menu', methods=['POST'])
def add_dish():
    # print("1")
    dish = request.json
    # print(dish)
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


# Endpoint for adding feedback to a dish
@app.route('/menu/<int:dish_id>/feedback', methods=['POST'])
def add_feedback(dish_id):
    feedback = request.json
    if 'rating' in feedback and 'comment' in feedback:
        conn = connect()
        cursor = conn.cursor()

        # Check if the dish exists
        cursor.execute("SELECT id FROM stocks WHERE id = %s", (dish_id,))
        dish = cursor.fetchone()
        if not dish:
            conn.close()
            return jsonify({'error': 'Dish not found'})

        # Insert feedback into the database
        cursor.execute("""
            INSERT INTO feedback (dish_id, rating, comment)
            VALUES (%s, %s, %s)
        """, (dish_id, feedback['rating'], feedback['comment']))

        conn.commit()
        conn.close()
        return jsonify({'message': 'Feedback added successfully'})
    else:
        return jsonify({'error': 'Invalid feedback data'})

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

@app.route('/menu/<int:dish_id>/feedback', methods=['GET'])
def get_feedback(dish_id):
    conn = connect()
    cursor = conn.cursor()

    # Retrieve feedback for the dish from the database
    cursor.execute("""
        SELECT rating, comment FROM feedback
        WHERE dish_id = %s
    """, (dish_id,))
    feedback = cursor.fetchall()

    conn.close()
    return jsonify(feedback)


@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = orders.get(order_id)
    if order:
        return jsonify(order)
    return 'Order not found', 404

# @app.route('/orders/<int:order_id>', methods=['PUT'])
# def update_order(order_id):
#     print("==-=-=-=-=----=-=-=--=-")
#     order = orders.get(order_id)
#     if order:
#         status = request.json.get('status')
#         if status:
#             order['status'] = status
#             print(status)
#             socketio.emit('order_status_updated', {'order_id': order_id, 'status': status}, broadcast=True)
#             return 'Order status updated successfully'
#         return 'No status provided', 400
#     return 'Order not found', 404

@socketio.on('update_order_status')
def handle_update_order_status(data):
    print(data)
    order_id = int(data['order_id'])
    status = data['status']

    
    if order_id in orders:
        # Update the status of the order
        orders[order_id]['status'] = status
   

        # Save the updated order
    saveOrder()
    # Emit the 'order_status_updated' event to all connected clients
    emit('order_status_updated', {'order_id': order_id, 'status': status}, broadcast=True)


# Save menu to the database
def saveMenu():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM stocks")
    for dish_id, dish in stocks.items():
        cursor.execute("""
            INSERT INTO stocks (id, name, price, available, stock)
            VALUES (%s, %s, %s, %s, %s)
        """, (dish_id, dish['name'], dish['price'], dish['available'], dish['stock']))

    conn.commit()
    conn.close()

# Load menu from the database
def loadMenu():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM stocks")
    for row in cursor.fetchall():
        dish_id = row[0]
        dish = {
            'name': row[1],
            'price': float(row[2]),
            'available': row[3],
            'stock': int(row[4])
        }
        stocks[dish_id] = dish

    conn.close()
 
# Save orders to the database
def saveOrder():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM orders")
    for order_id, order in orders.items():
        cursor.execute("""
            INSERT INTO orders (id, customer, status)
            VALUES (%s, %s, %s)
        """, (order_id, order['customer'], order['status']))

    conn.commit()
    conn.close()

# Load orders from the database
def loadOrders():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM orders")
    for row in cursor.fetchall():
        order_id = row[0]
        order = {
            'customer': row[1],
            'status': row[2]
        }
        orders[order_id] = order

    conn.close()


def load_data():
    create_stocks_table()
    create_orders_table()
    create_feedback_table()

    loadMenu()
    loadOrders()
  
# @socketio.on('update_order_status')
# def handle_update_order_status(data):
#     print('Received update_order_status event')
#     print(data)
#     # Perform any necessary actions based on the received data


if __name__ == '__main__':
    load_data()
    socketio.run(app,host='0.0.0.0',port=5000)
