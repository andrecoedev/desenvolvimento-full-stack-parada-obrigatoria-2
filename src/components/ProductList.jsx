import React from 'react';
import { useDispatch } from 'react-redux';

export default function ProductList({ products }) {
  const dispatch = useDispatch();
  return (
    <>
      <p className="eyebrow">Explore a coleção</p>
      <h1 tabIndex={-1}>Seu próximo livro está aqui.</h1>
      <p className="intro">Escolha um título e adicione ao seu carrinho.</p>
      <ul className="product-list">
        {products.map(product => (
          <li key={product.id} className="product-card">
            <img src={product.cover} alt={`Capa ilustrativa do livro ${product.name}`} width="200" height="260" />
            <div>
              <h2>{product.name}</h2>
              <p>Livro do catálogo de demonstração.</p>
              <button type="button" aria-label={`Adicionar ao carrinho: ${product.name}`}
                onClick={() => dispatch({ type: 'ADD_TO_CART', payload: product })}>Adicionar ao carrinho</button>
            </div>
          </li>
        ))}
      </ul>
    </>
  );
}
