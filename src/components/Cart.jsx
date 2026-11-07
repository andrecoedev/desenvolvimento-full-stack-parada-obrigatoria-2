import React, { useEffect, useRef } from 'react';
import { Link } from 'react-router-dom';
import { useSelector, useDispatch } from 'react-redux';

export default function Cart() {
  const cart = useSelector(state => state.cart);
  const dispatch = useDispatch();
  const titleRef = useRef(null);
  const removed = useRef(false);

  useEffect(() => {
    if (removed.current) {
      titleRef.current.focus();
      removed.current = false;
    }
  }, [cart]);

  function removeFromCart(item) {
    removed.current = true;
    dispatch({ type: 'REMOVE_FROM_CART', payload: item });
  }

  // A base remove todas as cópias de um mesmo título. A lista agrupa essas cópias.
  const titles = cart.filter((item, index) => cart.findIndex(book => book.id === item.id) === index);
  return (
    <>
      <p className="eyebrow">Sua seleção</p>
      <h1 tabIndex={-1} ref={titleRef}>Seu carrinho</h1>
      <p className="intro">{cart.length === 0 ? 'Seu carrinho está vazio.' : `${cart.length} livro(s) no carrinho.`}</p>
      {titles.length > 0 && <ul className="cart-list">
        {titles.map(item => (
          <li key={item.id} className="cart-item">
            <div><h2>{item.name}</h2><p>Quantidade: {cart.filter(book => book.id === item.id).length}</p></div>
            <button type="button" className="secondary" aria-label={`Remover do carrinho: todas as cópias de ${item.name}`}
              onClick={() => removeFromCart(item)}>Remover do carrinho</button>
          </li>
        ))}
      </ul>}
      <Link className="back-link" to="/">Continuar escolhendo livros</Link>
    </>
  );
}
