// Retrieve the DOM elements
//socket


const viewMenuBtn = document.getElementById('viewMenuBtn');
const viewOrdersBtn = document.getElementById('viewOrdersBtn');
const addDishBtn = document.getElementById('addDishBtn');
const updateDishBtn = document.getElementById('updateDishBtn');
const takeOrderBtn = document.getElementById('takeOrderBtn');
const viewOrderBtn = document.getElementById('viewOrderBtn');
const updateStatusBtn = document.getElementById('updateStatusBtn');
const rightColumn = document.querySelector('.right-column');





// Event listeners for button clicks
viewMenuBtn.addEventListener('click', () => {
    var rightColumn = document.querySelector('.right-column');
    rightColumn.style.backgroundImage = 'none';
  fetchMenu();
});

viewOrdersBtn.addEventListener('click', () => {
  fetchOrders();
});

addDishBtn.addEventListener('click', () => {
  displayAddDishForm();
});

updateDishBtn.addEventListener('click', () => {
  displayUpdateDishForm();
});

takeOrderBtn.addEventListener('click', () => {
  displayTakeOrderForm();
});

viewOrderBtn.addEventListener('click', () => {
  displayViewOrderForm();
});

updateStatusBtn.addEventListener('click', () => {
  displayUpdateStatusForm();
});



// Functions to fetch data or display forms
function fetchMenu() {
  fetch('http://localhost:5000/menu')
    .then(response => response.json())
    .then(data => {
      const menuContent = createMenuContent(data);
      displayContent(menuContent);
    })
    .catch(error => console.log(error));
}

function fetchOrders() {
  fetch('http://localhost:5000/orders')
    .then(response => response.json())
    .then(data => {
      const ordersContent = createOrdersContent(data);
      displayContent(ordersContent);
    })
    .catch(error => console.log(error));
}

function displayAddDishForm() {
  const addDishForm = `
    <h2>Add Dish</h2>
    <form id="addDishForm">
      <label for="name">Name:</label>
      <input type="text" id="name" required>
      <br>
      <label for="price">Price:</label>
      <input type="number" id="price" required>
      <br>
      <label for="available">Available:</label>
      <select id="available" required>
        <option value="yes">Yes</option>
        <option value="no">No</option>
      </select>
      <br>
      <label for="stock">Stock:</label>
      <input type="number" id="stock" required>
      <br>
      <button type="submit">Add</button>
    </form>
  `;

  displayContent(addDishForm);

  const addDishFormElement = document.getElementById('addDishForm');
  addDishFormElement.addEventListener('submit', (event) => {
    event.preventDefault();
    const name = document.getElementById('name').value;
    const price = document.getElementById('price').value;
    const available = document.getElementById('available').value;
    const stock = document.getElementById('stock').value;

    const dish = {
      name: name,
      price: price,
      available: available,
      stock: stock
};

    addDish(dish);
  });
}

function displayUpdateDishForm() {
  const updateDishForm = `
    <h2>Update Dish</h2>
    <form id="updateDishForm">
      <label for="dishId">Dish ID:</label>
      <input type="number" id="dishId" required>
      <br>
      <button type="submit">Update</button>
    </form>
  `;

  displayContent(updateDishForm);

  const updateDishFormElement = document.getElementById('updateDishForm');
  updateDishFormElement.addEventListener('submit', (event) => {
    event.preventDefault();
    const dishId = document.getElementById('dishId').value;

    updateDish(dishId);
  });
}

function displayTakeOrderForm() {
    const takeOrderForm = `
      <h2>Take Order</h2>
      <form id="takeOrderForm">
        <label for="customer">Customer:</label>
        <input type="text" id="customer" required>
        <br>
        <div id="item-list">
          <div class="item-row">
            <label for="dish-qty-1">Dish ID - Quantity:</label>
            <input type="text" id="dish-qty-1" required>
          </div>
        </div>
        <button type="button" id="add-item-btn">Add Item</button>
        <br>
        <button type="submit">Take Order</button>
      </form>
    `;
  
    displayContent(takeOrderForm);
  
    const itemList = document.getElementById('item-list');
    const addItemBtn = document.getElementById('add-item-btn');
    let itemId = 2; // Starting ID for dynamically added item rows
  
    addItemBtn.addEventListener('click', () => {
      const itemRow = document.createElement('div');
      itemRow.className = 'item-row';
  
      const label = document.createElement('label');
      label.for = `dish-qty-${itemId}`;
      label.textContent = 'Dish ID - Quantity: ';
      itemRow.appendChild(label);
  
      const input = document.createElement('input');
      input.type = 'text';
      input.id = `dish-qty-${itemId}`;
      input.required = true;
      itemRow.appendChild(input);
  
      itemList.appendChild(itemRow);
  
      itemId++;
    });
  
    const takeOrderFormElement = document.getElementById('takeOrderForm');
    takeOrderFormElement.addEventListener('submit', (event) => {
      event.preventDefault();
      const customer = document.getElementById('customer').value;
      const items = [];
  
      // Get values from all dish-qty input fields
      const dishQtyInputs = document.querySelectorAll('[id^="dish-qty-"]');
      dishQtyInputs.forEach((input) => {
        const [dishId, quantity] = input.value.split('-').map(value => value.trim());
        if (dishId && quantity) {
          items.push({ dish_id: parseInt(dishId), quantity: parseInt(quantity) });
        }
      });
  
      const order = {
        customer: customer,
        items: items
      };
  
      takeOrder(order);
    });
  }
  

function displayViewOrderForm() {
  const viewOrderForm = `
    <h2>View Order</h2>
    <form id="viewOrderForm">
      <label for="orderId">Order ID:</label>
      <input type="number" id="orderId" required>
      <br>
      <button type="submit">View Order</button>
    </form>
  `;

  displayContent(viewOrderForm);

  const viewOrderFormElement = document.getElementById('viewOrderForm');
  viewOrderFormElement.addEventListener('submit', (event) => {
    event.preventDefault();
    const orderId = document.getElementById('orderId').value;

    viewOrder(orderId);
  });
}

function displayUpdateStatusForm() {
  const updateStatusForm = `
    <h2>Update Order Status</h2>
    <form id="updateStatusForm">
      <label for="orderId">Order ID:</label>
      <input type="number" id="orderId" required>
      <br>
      <label for="status">Status:</label>
      <input type="text" id="status" required>
      <br>
      <button type="submit">Update Status</button>
    </form>
  `;

  displayContent(updateStatusForm);

  const updateStatusFormElement = document.getElementById('updateStatusForm');
  updateStatusFormElement.addEventListener('submit', (event) => {
    event.preventDefault();
    const orderId = document.getElementById('orderId').value;
    const status = document.getElementById('status').value;

    updateOrderStatus(orderId, status);
  });
}

function addDish(dish) {
    fetch('http://localhost:5000/menu', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(dish)
  })
    .then(response => response.json())
    .then(data => {
      displayMessage(data.message);
      fetchMenu();
    })
    .catch(error => console.log(error));
}

function updateDish(dishId) {
  fetch(`http://localhost:5000/menu/${dishId}`, {
    method: 'PUT'
  })
    .then(response => response.json())
    .then(data => {
      displayMessage(data.message);
      fetchMenu();
    })
    .catch(error => console.log(error));
}

function takeOrder(order) {
    console.log(order)
  fetch('http://localhost:5000/orders', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(order)
  })
    .then(response => response.json())
    .then(data => {
      displayMessage(data.message);
      fetchOrders();
    })
    .catch(error => console.log(error));
}

function viewOrder(orderId) {
  fetch(`http://localhost:5000/orders/${orderId}`)
    .then(response => {
      if (response.status === 404) {
        throw new Error('Order not found');
      }
      return response.json();
    })
    .then(data => {
      const orderContent = createOrderContent(data,orderId);
      displayContent(orderContent);
    })
    .catch(error => {
      const errorMessage = `<p>${error.message}</p>`;
      displayContent(errorMessage);
    });
}




// function updateOrderStatus(orderId, status) {
//   fetch(`http://localhost:5000/orders/${orderId}`, {
//     method: 'PUT',
//     headers: {
//       'Content-Type': 'application/json'
//     },
//     body: JSON.stringify({ status: status })
//   })
//     .then(response => {
//       if (response.status === 404) {
//         throw new Error('Order not found');
//       }
//       return response.text();
//     })
//     .then(data => {
//       displayMessage(data);
//       fetchOrders();
//     })
//     .catch(error => console.log(error));
// }

// Helper functions for creating HTML content

const socket = io("ws://127.0.0.1:5000");
socket.on('connect', () => {
  console.log('Connected to WebSocket');
});

socket.on('disconnect', () => {
  console.log('Disconnected from WebSocket');
});

socket.on('order_status_updated', (data) => {
  const { order_id, status } = data;
  // Update the UI with the new order status
  // console.log(data);
  fetchOrders()
  displayMessage(data)
});



function updateOrderStatus(orderId, status) {
  
  socket.emit('update_order_status', { order_id: orderId, status: status });
  console.log(orderId,status)
}


function createMenuContent(menuData) {
  let menuContent = '<h2>Menu</h2>';
  for (const dishId in menuData) {
    const dish = menuData[dishId];
    menuContent += `
      <div class="dish">
        <h3>${dish.name}</h3>
        <p>Price: ${dish.price}</p>
        <p>Available: ${dish.available}</p>
        <p>Stock: ${dish.stock}</p>
        <button class="remove-dish-btn" data-dish-id="${dishId}">Remove Dish</button>
     
        <button class="show-feedback-btn" data-dish-id="${dishId}">Show Feedback</button>
        <button class="add-feedback-btn" data-dish-id="${dishId}">Add Feedback</button>
        
        </div>
    `;
  }
  return menuContent;
}

  

  function createOrdersContent(orders) {
    let ordersContent = '<h2>Orders</h2>';
    if (Object.keys(orders).length > 0) {
      ordersContent += '<ul class="orders-list">';
      for (const [orderId, order] of Object.entries(orders)) {
        const statusClass = getStatusClass(order.status);
        ordersContent += `
          <li class="order-item ${statusClass}">
            <span class="order-id">Order ID: ${orderId}</span>
            <span class="order-customer">Customer: ${order.customer}</span>
            <span class="order-status">Status: ${order.status}</span>
          </li>
        `;
      }
      ordersContent += '</ul>';
    } else {
      ordersContent += '<p>No orders available.</p>';
    }
    return ordersContent;
  }
  
  // Helper function to determine the CSS class based on order status
  function getStatusClass(status) {
    let statusClass = '';
    if (status === 'received') {
      statusClass = 'received';
    } else if (status === 'ready') {
      statusClass = 'ready';
    } else if (status === 'preparing') {
      statusClass = 'preparing';
    }
    return statusClass;
  }
  

// Event listener for removing a dish
rightColumn.addEventListener('click', (event) => {
    if (event.target.classList.contains('remove-dish-btn')) {
      const dishId = event.target.dataset.dishId;
      removeDish(dishId);
    }
  });
  
  // Function to remove a dish
  function removeDish(dishId) {
    fetch(`http://localhost:5000/menu/${dishId}`, {
      method: 'DELETE'
    })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          fetchMenu(); // Refresh the menu after successful removal
        } else {
          console.log(data.message);
        }
      })
      .catch(error => console.log(error));
  }

function createOrderContent(order,orderId) {
    // console.log(order)
  let orderContent = '<h2>Order Details</h2>';
  orderContent += `<p>Order ID: ${orderId}</p>`;
  orderContent += `<p>Customer: ${order.customer}</p>`;
  orderContent += '<p>Order Items:</p>';
  orderContent += '<ul>';
  for (const item of order.order) {
    orderContent += `<li>Dish: ${item.dish}, Quantity: ${item.quantity}</li>`;
  }
  orderContent += '</ul>';
  orderContent += `<p>Status: ${order.status}</p>`;
  return orderContent;
}

function fetchFeedback(dishId) {
  fetch(`http://localhost:5000/menu/${dishId}/feedback`)
    .then(response => response.json())
    .then(data => {
      const feedbackContent = createFeedbackContent(data);
      displayContent(feedbackContent);
    })
    .catch(error => console.log(error));
}
function createFeedbackContent(feedbackData) {
  console.log(feedbackData)
  let feedbackContent = '<h2>Feedback</h2>';
  for (const feedback of feedbackData) {
    feedbackContent += `
      <div class="feedback">
        <p>Rating: ${feedback[0]}</p>
        <p>Comment: ${feedback[1]}</p>
      </div>
    `;
  }
  return feedbackContent;
}

function displayContent(content) {
  rightColumn.innerHTML = content;
  const showFeedbackBtns = document.querySelectorAll('.show-feedback-btn');
showFeedbackBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    const dishId = btn.dataset.dishId;
    fetchFeedback(dishId);
  });
});

const addFeedbackBtns = document.querySelectorAll('.add-feedback-btn');
addFeedbackBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    const dishId = btn.dataset.dishId;
    displayAddFeedbackForm(dishId);
  });
});
}

function displayMessage(message) {
  const messageElement = document.createElement('p');
  messageElement.textContent = message;
  rightColumn.innerHTML = '';
  rightColumn.appendChild(messageElement);
}


function displayAddFeedbackForm(dishId) {
  const addFeedbackForm = `
    <h2>Add Feedback</h2>
    <form id="addFeedbackForm">
      <input type="hidden" id="dishId" value="${dishId}">
      <label for="rating">Rating:</label>
      <input type="number" id="rating" min="1" max="5" required>
      <br>
      <label for="comment">Comment:</label>
      <textarea id="comment" required></textarea>
      <br>
      <button type="submit">Submit</button>
    </form>
  `;

  displayContent(addFeedbackForm);

  const addFeedbackFormElement = document.getElementById('addFeedbackForm');
  addFeedbackFormElement.addEventListener('submit', (event) => {
    event.preventDefault();
    const rating = document.getElementById('rating').value;
    const comment = document.getElementById('comment').value;
    const feedback = {
      dish_id: dishId,
      rating: rating,
      comment: comment
    };
    submitFeedback(feedback);
  });
}
function submitFeedback(feedback) {
  const dishId = feedback.dish_id; // Assuming you have a `dish_id` property in the feedback object
  fetch(`http://localhost:5000/menu/${dishId}/feedback`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(feedback)
  })
    .then(response => response.json())
    .then(data => {
      displayMessage(data.message);
    })
    .catch(error => console.log(error));
}

