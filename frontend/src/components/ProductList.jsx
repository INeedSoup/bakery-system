import React, { useEffect, useState } from 'react';
import axios from 'axios';

export default function ProductList() {
  const [products, setProducts] = useState([]);
  useEffect(() => {
    axios.get(`${process.env.REACT_APP_API_URL}/products`)
      .then(res => setProducts(res.data))
      .catch(console.error);
  }, []);
  return (
    <div>
      <h2>Products</h2>
      <ul>
        {products.map(p => (
          <li key={p.id}>{p.name} — ₹{p.price}</li>
        ))}
      </ul>
    </div>
  );
}
