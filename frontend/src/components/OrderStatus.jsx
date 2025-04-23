import React, { useState } from 'react';
import axios from 'axios';

export default function OrderStatus() {
  const [id, setId] = useState('');
  const [order, setOrder] = useState(null);

  const check = () => {
    axios.get(`${process.env.REACT_APP_API_URL}/orders/${id}`)
      .then(res => setOrder(res.data))
      .catch(err => alert(err.response?.data?.detail || err));
  };

  return (
    <div>
      <h2>Check Order</h2>
      <input
        type="number" placeholder="Order ID"
        value={id} onChange={e => setId(e.target.value)} />
      <button onClick={check} disabled={!id}>Check</button>
      {order && (
        <p>
          #{order.id}: {order.product.name} × {order.quantity}<br/>
          Status: {order.status}<br/>
          Placed: {new Date(order.created_at).toLocaleString()}
        </p>
      )}
    </div>
  );
}
