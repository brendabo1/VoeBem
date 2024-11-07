import React from 'react';
import axios from 'axios';
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

function ComprarPassagem({ userId, trechosSelecionados }) {
  const realizarCompra = async () => {
    try {
      const response = await axios.post(`${process.env.REACT_APP_BACKEND_URL}/comprar_passagem`, {
        user_id: userId,
        trechos: trechosSelecionados
      });

      // Verifica o status da resposta
      if (response.status === 200) {
        toast.success(response.data.message || "Compra realizada com sucesso!");
      } else {
        toast.error(response.data.message || "Erro ao realizar a compra.");
      }
    } catch (error) {
      // Caso haja um erro durante a requisição
      if (error.response && error.response.data && error.response.data.message) {
        toast.error(error.response.data.message);
      } else {
        toast.error("Ocorreu um erro inesperado durante a compra.");
      }
    }
  };

  return (
    <div>
      <button onClick={realizarCompra}>Comprar Passagem</button>
      <ToastContainer position="top-right" autoClose={5000} hideProgressBar />
    </div>
  );
}

export default ComprarPassagem;
