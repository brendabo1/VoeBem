// cliente-react/src/components/Menu.js
import React from 'react';
import { Link } from 'react-router-dom';
import './Menu.css';

const Menu = () => {
    return (
        <div className="menu-container">
            {/* <h2>Decolar nunca foi tão simples</h2> 
            <h2>Sua próxima aventura começa aqui!</h2> */}
            <p>Escolha uma das opções abaixo:</p>
            <ul className="menu-options">
                <li><Link to="/supergrafo">Todas as Rotas</Link></li>
                <li><Link to="/buscar_rotas">Buscar Rotas</Link></li>
                <li><Link to="/pedidos">Meus Pedidos</Link></li>
            </ul>
        </div>
    );
};

export default Menu;
