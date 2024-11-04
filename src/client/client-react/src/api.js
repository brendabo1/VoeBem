// src/api.js
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL;

export const login = async (id, senha) => {
    try {
        const response = await axios.post(`${API_URL}/login`, { id, senha });
        return response.data;  // Retorna os dados da resposta em caso de sucesso
    } catch (error) {
        if (error.response && error.response.status === 401) {
            throw new Error("ID ou senha incorretos");
        }
        throw new Error("Erro ao realizar o login");
    }
};

export const listarSupergrafo = () => {
    return axios.get(`${API_URL}/listar_supergrafo`);
};

export const reservarAssentos = (origem, destino, assentos) => {
    return axios.post(`${API_URL}/reservar_assentos`, { origem, destino, assentos });
};
