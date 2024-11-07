// src/api.js
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_BACKEND_URL;

const api = axios.create({
    baseURL: process.env.REACT_APP_BACKEND_URL
});

export const login = async (id, senha) => {
    try {
        const response = await api.post('/login', { id, senha });  // Use api.post ao invés de axios.post
        return response.data;
    } catch (error) {
        console.error(error.response || error); 
        if (error.response && error.response.status === 401) {
            throw new Error("ID ou senha incorretos");
        }
        throw new Error("Erro ao realizar o login");
    }
};

export const fetchSupergrafo = async () => {
    try {
        const response = await api.get('/supergrafo');
        return response.data.supergrafo;
    } catch (error) {
        console.error("Erro ao buscar supergrafo:", error);
        throw error;
    }
};

export const buscarRotas = async (origem, destino) => {
    try {
        const response = await api.post('/buscar_rotas', { origem, destino });  // Use api.post ao invés de axios.post
        return response.data.rotas;
    } catch (error) {
        throw new Error("Erro ao buscar rotas");
    }
};

export const selecionaAssentos = async (rotaSelecionada) => {
    const response = await axios.post('/selec_assento', { rota: rotaSelecionada });
    return response.data;
};

export const confirmarCompra = async (assentosSelecionados) => {
    const response = await axios.post('/confirmar_compra', { assentos: assentosSelecionados });
    return response.data;
};

// export const enviarRotaSelecionada = async (rota) => {
//     const response = await axios.post('/comprar_rota', { rota });
//     return response.data;
// };

export const realizarCompra = async (listaDeTrechos, userId) => {
    const url = `${process.env.REACT_APP_BACKEND_URL}/comprar_passagem`;
    const response = await axios.post(url, {
        user_id: userId,
        trechos: listaDeTrechos,
    });
    return response.data;
};

export const obterPedidos = async (userId) => {
    try {
        const response = await axios.get(`${API_BASE_URL}/pedidos/${userId}`);
        return response.data;
    } catch (error) {
        console.error('Erro ao buscar pedidos do usuário:', error);
        throw error;
    }
};

// export const comprarPassagem = async (user_id, trechos) => {
//     try {
//         const response = await api.post('/comprar_passagem', { user_id, trechos });  
//         return response.data.message;
//     } catch (error) {
//         throw new Error(error.response?.data.message || "Erro ao comprar passagem");
//     }
// };

// export const reservarAssentos = (origem, destino, assentos) => {
//     return api.post('/reservar_assentos', { origem, destino, assentos });  // Use api.post ao invés de axios.post
// };
