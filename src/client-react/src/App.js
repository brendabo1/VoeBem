// cliente-react/src/App.js
import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Home from './components/Home';
import Login from './components/Login';
import Menu from './components/Menu';
import Supergrafo from './components/Supergrafo';
import Pedidos from './components/Pedidos';
import Header from './components/Header';
import BuscaRotas from './components/Busca';
import SelecionaAssento from './components/SelecionaAssento';
import ComprarPassagem from './components/ComprarPassagem';
import './App.css';


function App() {
    const [loggedIn, setLoggedIn] = useState(false);
    const [userId, setUserId] = useState('');
    // const [origem, setOrigem] = useState('');
    // const [destino, setDestino] = useState('');
    const [trechosSelecionados, setTrechosSelecionados] = useState([]);

    const handleLoginSuccess = (id) => {
        setLoggedIn(true);
        setUserId(id);
    };
    

    return (   
        <Router>
            <div>
                <Header />
                <Routes>
                    <Route path="/" element={<Home />} />
                    <Route path="/login" element={<Login onLoginSuccess={handleLoginSuccess} />} />
                    <Route path="/dashboard" element={loggedIn ? <Menu /> : <Navigate to="/login" />} />

                    {/* Rotas para funcionalidades do sistema, acessíveis apenas se logado */}
                    {loggedIn && (
                        <>
                        <Route path="/buscar_rotas" element={<BuscaRotas/>} />
                        <Route path="/comprar_passagem" element={<ComprarPassagem userId={userId} trechosSelecionados={trechosSelecionados} />} />
                        <Route path="/selec_assento" element={<SelecionaAssento user_id={userId} trechos={trechosSelecionados} />} /> 
                        <Route path="/supergrafo" element={<Supergrafo />} />
                        <Route path="/pedidos" element={<Pedidos userId={userId} />} />
                        </>
                    )}

                    {/* Redirecionamento para login se tentar acessar rota protegida */}
                    <Route path="*" element={<Navigate to={loggedIn ? "/dashboard" : "/login"} />} />
                </Routes>
            </div>
        </Router>
    );
}

export default App;
