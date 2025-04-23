import React, { useState, useEffect } from 'react';
import axios from 'axios';

export default function OrderForm() {
  const [products, setProducts] = useState([]);
  const [productId, setProductId] = useState('');
  const [qty, setQty] = useState(1);
  const [order, setOrder] = useState(null);

  useEffect(() => {
    axios.get(`${process.env.REACT_APP_API_URL}/products`)
      .then(res => setProducts(res.data))
      .catch(console.error);
  }, []);

  const submit = () => {
    axios.post(`${process.env.REACT_APP_API_URL}/orders`, { product_id: +productId, quantity: qty })
      .then(res => setOrder(res.data))
      .catch(err => alert(err.response?.data?.detail || err));
  };

  return (
    <div>
      <h2>Place Order</h2>
      <select value={productId} onChange={e => setProductId(e.target.value)}>
        <option value="">-- Select Product --</option>
        {products.map(p => (
          <option key={p.id} value={p.id}>{p.name}</option>
        ))}
      </select>
      <input type="number" value={qty} min="1" onChange={e => setQty(+e.target.value)} />
      <button onClick={submit} disabled={!productId}>Order</button>
      {order && <p>Order #{order.id} placed! Status: {order.status}</p>}
    </div>
  );
}
