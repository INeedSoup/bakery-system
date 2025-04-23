import React from 'react';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import ProductList from './components/ProductList';
import OrderForm from './components/OrderForm';
import OrderStatus from './components/OrderStatus';

export default function App() {
  return (
    <BrowserRouter>
      <nav className="container">
        <Link to="/">Home</Link> |{' '}
        <Link to="/order">Place Order</Link> |{' '}
        <Link to="/status">Check Order</Link>
      </nav>
      <div className="container">
        <h1>Bakery System</h1>
        <Routes>
          <Route path="/" element={<ProductList />} />
          <Route path="/order" element={<OrderForm />} />
          <Route path="/status" element={<OrderStatus />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}
