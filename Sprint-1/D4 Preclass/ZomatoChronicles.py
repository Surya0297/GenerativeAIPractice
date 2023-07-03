import json
import re

stocks = {}
orders = {}

def saveMenu():
    with open("Sprint-1/D4 Preclass/menu.txt", "w") as file:
        for key, value in stocks.items():
            file.write(f"{key}:{value['name']},{value['price']},{value['available']},{value['stock']}\n")
    print("Menu updated.")

def loadMenu():
    try:
        with open('Sprint-1/D4 Preclass/menu.txt', "r") as file:
            for line in file:
                line = line.strip()
                key, data = line.split(":")
                name, price, availability, stock_qty = data.split(",")
                stocks[int(key)] = {
                    'name': name,
                    'price': float(price),
                    'available': availability,
                    'stock': int(stock_qty)
                }
        print("Menu data loaded from file.")
    except FileNotFoundError:
        print("Menu data file not found. Starting with an empty menu.")

def addDish():
    if len(stocks) > 0:
        last_key = list(stocks.keys())[-1]
    else:
        last_key = 0

    name = input("Enter dish name: ")
    price = input("Enter dish price: ")
    available = input("Enter dish availability: ")
    stock = input("Enter stock available: ")

    dish = {'name': name, 'price': price, 'available': available, 'stock': stock}
    stocks[last_key + 1] = dish
    print("Dish added")
    saveMenu()

def viewStock():
    if len(stocks) > 0:
        print("Dish ID | Dish Name            | Price | Availability | Stock")
        print("-" * 65)
        for dish_id, dish_data in stocks.items():
            print(f"{dish_id:<8} | {dish_data['name']:<20} | {dish_data['price']:<5} | {dish_data['available']:<12} | {dish_data['stock']}")
    else:
        print("No Dishes In Stock")



def updateDish():
    id = int(input("Enter dish id: "))
    if id not in stocks:
        print("Dish with this id does not exist")
        return
    dish = stocks[id]
    if dish['available'] == 'yes':
        dish['available'] = 'no'
    else:
        dish['available'] = 'yes'
    print('Dish Availability Updated')
    saveMenu()

def removeDish():
    id = int(input("Enter Dish id: "))
    if id not in stocks:
        print("Dish with this id does not exist.")
        return
    del stocks[id]
    saveMenu()
    print("**** Dish deleted ****")

def saveOrder():
    # print(orders)
    with open("Sprint-1/D4 Preclass/order.txt", "w") as file:
        for order_id, order_data in orders.items():
            order_items = "/".join([f'{{"dish": "{dish["dish"]}", "quantity": {dish["quantity"]}}}' for dish in order_data['order']])
            file.write(f"{order_id}/{order_data['customer']}/{order_items}/{order_data['status']}\n")
            # file.write("ok")

    print("Order data saved to file.")



def takeOrder():
    customer_name = input("Enter Customer Name: ")
    order_list = []
    order = input("Enter Dish id-quantity (comma-separated): ")
    order_items_list = order.split(',')
    for order_item in order_items_list:
        item = order_item.split('-')
        dish_id = int(item[0])
        quantity = int(item[1])
        if dish_id in stocks:
            dish = stocks[dish_id]
            if dish['available'] == 'yes' and quantity <= dish['stock']:
                dish['stock'] -= quantity
                order_list.append({'dish': dish['name'], 'quantity': quantity})
                if dish['stock'] == 0:
                    dish['available'] = 'no'
            else:
                print(dish['name'], "cannot be added as it is out of stock")
        else:
            print("Dish with id", dish_id, "does not exist")

    if len(orders) == 0:
        order_id = 1
    else:
        order_id = int(max(orders.keys())) + 1
    
    orders[order_id] = {'customer': customer_name, 'order': order_list, 'status': 'received'}

    saveOrder()  
    saveMenu()
    # print(orders)
    print('Order Successful')

def viewOrders():
    if len(orders) > 0:
        # Define the column headers
        order_id_header = "Order ID"
        customer_header = "Customer"
        order_header = "Order"
        status_header = "Status"

        # Calculate the maximum width for each column
        max_order_id_width = max(len(order_id_header), max(len(str(order_id)) for order_id in orders.keys()))
        max_customer_width = max(len(customer_header), max(len(order_data['customer']) for order_data in orders.values()))
        max_order_width = max(len(order_header), max(len(f"{item['dish']}: {item['quantity']}\n") for order_data in orders.values() for item in order_data['order']))
        max_status_width = max(len(status_header), max(len(order_data['status']) for order_data in orders.values()))

        # Create the table header
        header = f"{order_id_header:<{max_order_id_width}} | {customer_header:<{max_customer_width}} | {order_header:<{max_order_width}} | {status_header:<{max_status_width}}"

        # Print the table header
        print(header)
        print("-" * len(header))

        # Print each row of the table
        for order_id, order_data in orders.items():
            order_items = "\n".join([f"{item['dish']}: {item['quantity']}" for item in order_data['order']])
            row = f"{order_id:<{max_order_id_width}} | {order_data['customer']:<{max_customer_width}} | {order_items:<{max_order_width}} | {order_data['status']:<{max_status_width}}"
            print(row)
    else:
        print("No Orders Data Present")

def loadOrders():
    with open("Sprint-1/D4 Preclass/order.txt", "r") as file:
        for data_string in file:
            order_id, customer, items, status = data_string.strip().split('/')

            entries = re.findall(r'\{.*?\}', items)
            entry_list = []
            for entry in entries:
                entry_dict = json.loads(entry)
                entry_list.append(entry_dict)

            orders[order_id] = {'customer': customer, 'order': entry_list, 'status': status}

def showMenu():
    loadMenu()
    viewStock()

def menu():
    # loadOrders()
    while True:
        print('0: Show Menu')
        print('1: Add Dish')
        print('2: Update Dish')
        print('3: Remove Dish')
        print('4: Take Order')
        print('5: View Stock')
        print('6: View Orders')
        print('7: Exit')

        choice = int(input("Enter Choice: "))

        if choice == 0:
            showMenu()
            print()
        elif choice == 1:
            addDish()
            print()
        elif choice == 2:
            updateDish()
            print()
        elif choice == 3:
            removeDish()
            print()
        elif choice == 4:
            takeOrder()
            print()
        elif choice == 5:
            viewStock()
            print()
        elif choice == 6:
            viewOrders()
            print()
        elif choice == 7:
            print("*** Thanks for using our services ***")
            break

menu()
