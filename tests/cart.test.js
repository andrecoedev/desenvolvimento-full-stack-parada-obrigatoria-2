import { test } from 'node:test';
import assert from 'node:assert/strict';
import { cartReducer } from '../src/store.js';

const book = { id: 1, name: 'Book 1' };
const other = { id: 2, name: 'Book 2' };

test('adiciona cópias sem alterar o estado anterior e informa o total', () => {
  const initial = cartReducer(undefined, { type: 'INIT' });
  const first = cartReducer(initial, { type: 'ADD_TO_CART', payload: book });
  const second = cartReducer(first, { type: 'ADD_TO_CART', payload: book });
  assert.equal(initial.cart.length, 0);
  assert.equal(first.cart.length, 1);
  assert.deepEqual(second.cart, [book, book]);
  assert.match(second.message, /Book 1 adicionado.*Total: 2/);
});

test('remove todas as cópias do título selecionado e preserva outros livros', () => {
  const state = { cart: [book, other, book], message: '' };
  const result = cartReducer(state, { type: 'REMOVE_FROM_CART', payload: book });
  assert.deepEqual(result.cart, [other]);
  assert.equal(state.cart.length, 3);
  assert.match(result.message, /Book 1 removido.*Total: 1/);
});

test('o último livro pode ser removido e ações desconhecidas preservam o estado', () => {
  const result = cartReducer({ cart: [book], message: '' }, { type: 'REMOVE_FROM_CART', payload: book });
  assert.deepEqual(result.cart, []);
  assert.match(result.message, /Total: 0/);
  assert.equal(cartReducer(result, { type: 'UNKNOWN' }), result);
});
