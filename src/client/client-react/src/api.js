// src/api.js
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL;

export const login = (id, senha) => {
    return axios.post(`${API_URL}/login`, { id, senha });
};

export const listarSupergrafo = () => {
    return axios.get(`${API_URL}/listar_supergrafo`);
};

export const reservarAssentos = (origem, destino, assentos) => {
    return axios.post(`${API_URL}/reservar_assentos`, { origem, destino, assentos });
};
