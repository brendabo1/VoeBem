// src/components/Home.js
import React from 'react';
import { useNavigate } from 'react-router-dom';
import './Home.css'; // Arquivo de estilos para a tela inicial

const Home = () => {
    const navigate = useNavigate();

    const handleLoginRedirect = () => {
        navigate('/login');
    };

    return (
        <div className="home-container">
            <h1 className="title">Voe Bem - Sistema de Passagens</h1>
            <button className="btn btn-primary" onClick={handleLoginRedirect}>
                Fazer Login
            </button>
        </div>
    );
};

export default Home;
