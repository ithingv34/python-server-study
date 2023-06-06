import React, { useState, useEffect } from 'react';
import axios from 'axios';

const App = () => {
  const [orders, setOrders] = useState([]);

  useEffect(() => {
    const fetchOrders = async () => {
      try {
        const response = await axios.get('http://localhost:8001/orders');
        setOrders(prevOrders => [...prevOrders, response.data]);
      } catch (error) {
        console.error('Error fetching orders:', error);
      }
    };

    fetchOrders();
  }, []);

  return (
    <div>
      <h1>Orders</h1>
      {orders.map((order, index) => (
        <div key={index}>
          <h2>order {index + 1}</h2>
          <h3>Users:</h3>
          <ul>
            {order.users.map(user => (
              <li key={user.id}>{user.name}</li>
            ))}
          </ul>
          <h3>Products:</h3>
          <ul>
            {order.products.map(product => (
              <li key={product.id}>{product.name}</li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  );
};

export default App;