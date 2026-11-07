import React from 'react';
import { useSelector, useDispatch } from 'react-redux';

export default function Cart() {
  const cart = useSelector(state => state.cart);
  const dispatch = useDispatch();
  return (
    <div>
      <h2>Your Cart</h2>
      {cart.map(item => (
        <div key={item.id}>
          <span>{item.name}</span>
          <button onClick={() => dispatch({ type: 'REMOVE_FROM_CART', payload: item })}>Remove</button>
        </div>
      ))}
    </div>
  );
}
