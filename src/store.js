import { createStore } from 'redux';

const initialState = { cart: [], message: '' };

export function cartReducer(state = initialState, action) {
  switch (action.type) {
    case 'ADD_TO_CART': {
      const cart = [...state.cart, action.payload];
      return { ...state, cart, message: `${action.payload.name} adicionado ao carrinho. Total: ${cart.length} livro(s).` };
    }
    case 'REMOVE_FROM_CART': {
      const cart = state.cart.filter(item => item.id !== action.payload.id);
      return { ...state, cart, message: `${action.payload.name} removido do carrinho. Total: ${cart.length} livro(s).` };
    }
    default:
      return state;
  }
}

export default createStore(cartReducer);
