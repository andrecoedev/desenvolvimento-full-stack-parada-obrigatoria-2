import React, { useEffect, useRef } from 'react';
import { useSelector } from 'react-redux';
import { BrowserRouter, Routes, Route, NavLink, Link, useLocation } from 'react-router-dom';
import ProductList from './components/ProductList';
import Cart from './components/Cart';

const products = [
  { id: 1, name: 'Book 1', cover: '/capas/livro-1.svg' },
  { id: 2, name: 'Book 2', cover: '/capas/livro-2.svg' }
];

function Layout() {
  const { cart, message } = useSelector(state => state);
  const { pathname } = useLocation();
  const previousPath = useRef(pathname);
  const mainRef = useRef(null);

  useEffect(() => {
    document.title = `${pathname === '/cart' ? 'Carrinho' : pathname === '/' ? 'Catálogo' : 'Página não encontrada'} | Livraria online`;
    if (previousPath.current !== pathname) {
      mainRef.current.querySelector('h1')?.focus();
      previousPath.current = pathname;
    }
  }, [pathname]);

  return (
    <>
      <a className="skip-link" href="#conteudo">Pular para o conteúdo</a>
      <header>
        <div className="container header-content">
          <p className="brand">Livraria online<span>Um próximo capítulo para você.</span></p>
          <nav aria-label="Navegação principal">
            <NavLink to="/" end>Catálogo</NavLink>
            <NavLink to="/cart">Carrinho ({cart.length})</NavLink>
          </nav>
        </div>
      </header>
      <main id="conteudo" ref={mainRef} className="container" tabIndex={-1}>
        <Routes>
          <Route path="/" element={<ProductList products={products} />} />
          <Route path="/cart" element={<Cart />} />
          <Route path="*" element={<><h1 tabIndex={-1}>Página não encontrada</h1><Link to="/">Voltar ao catálogo</Link></>} />
        </Routes>
      </main>
      <div className="container status" role="status" aria-live="polite" aria-atomic="true">{message}</div>
      <footer className="container">Projeto acadêmico • Desenvolvimento Full Stack • SENAI</footer>
    </>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <Layout />
    </BrowserRouter>
  );
}
