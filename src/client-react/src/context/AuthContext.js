import React, { createContext, useContext, useState } from 'react';

// Criação do contexto
const AuthContext = createContext();

// Hook para acessar o contexto
export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null); // Aqui você define o estado do usuário logado

    // Função para logar o usuário (exemplo)
    const login = (userData) => {
        setUser(userData);
    };

    // Função para deslogar o usuário
    const logout = () => {
        setUser(null);
    };

    return (
        <AuthContext.Provider value={{ user, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
};
