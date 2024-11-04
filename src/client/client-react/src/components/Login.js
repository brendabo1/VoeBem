// src/components/Login.js
import React, { useState } from 'react';
import { login } from '../api';

const Login = ({ onLoginSuccess }) => {
    const [userId, setUserId] = useState('');
    const [senha, setSenha] = useState('');
    const [error, setError] = useState('');

    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            await login(userId, senha);
            onLoginSuccess();
        } catch (error) {
            setError('ID ou senha incorretos');
        }
    };

    return (
        <div className="container">
            <h2>Login</h2>
            <form onSubmit={handleLogin}>
                <div className="form-group">
                    <label>ID do Usuário</label>
                    <input type="text" className="form-control" value={userId} onChange={(e) => setUserId(e.target.value)} required />
                </div>
                <div className="form-group">
                    <label>Senha</label>
                    <input type="password" className="form-control" value={senha} onChange={(e) => setSenha(e.target.value)} required />
                </div>
                <button type="submit" className="btn btn-primary">Entrar</button>
                {error && <p className="text-danger">{error}</p>}
            </form>
        </div>
    );
};

export default Login;
