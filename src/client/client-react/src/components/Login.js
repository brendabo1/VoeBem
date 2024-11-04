// src/components/Login.js
import React, { useState } from 'react';
import { login } from '../api';
import './Login.css'; // Importando o arquivo CSS

const Login = ({ onLoginSuccess }) => {
    const [userId, setUserId] = useState('');
    const [senha, setSenha] = useState('');
    const [error, setError] = useState('');

    const handleLogin = async (e) => {
        e.preventDefault();
        setError('');  // Limpa o erro anterior
        try {
            await login(userId, senha);
            onLoginSuccess();  // Chama a função para navegar ao dashboard, etc.
        } catch (error) {
            setError(error.message);  // Define a mensagem de erro
        }
        // try {
        //     const response = await login(userId, senha);
        //     if (response.message === "Login bem-sucedido") {
        //         onLoginSuccess();
        //     } else {
        //         setError('ID ou senha incorretos');
        //     }
        // } catch (error) {
        //     setError('Erro ao realizar o login');
        // }
    };

    return (
        <div className="login-container">
            <h1 className="title">Voe Bem</h1>
            <div className="login-box">
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
        </div>
    );
};

export default Login;