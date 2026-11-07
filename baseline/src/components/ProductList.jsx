import React from 'react';
import { useDispatch } from 'react-redux';

export default function ProductList({ products }) {
  const dispatch = useDispatch();
  return (
    <div>
      {products.map(product => (
        <div key={product.id}>
          <h2>{product.name}</h2>
          <button onClick={() => dispatch({ type: 'ADD_TO_CART', payload: product })}>Add to Cart</button>
        </div>
      ))}
    </div>
  );
}
