import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { obterPedidos } from '../api';


const PedidosUsuario = ({ userId }) => {
    const [pedidos, setPedidos] = useState([]);
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchPedidos = async () => {
            try {
                const response = await obterPedidos(userId);
                setPedidos(response.pedidos);
            } catch (err) {
                setError('Erro ao buscar pedidos.');
            } finally {
                setLoading(false); // Define loading como false após o término da requisição
            }
        };

        fetchPedidos();
    }, [userId]);


    if (loading) return <p>Carregando pedidos...</p>;
    if (error) return <p>{error}</p>;

    return (
        <div>
            <h2>Pedidos de Reservas</h2>
            {pedidos.length > 0 ? (
                <ul>
                    {pedidos.map((pedido, index) => (
                        <li key={index}>
                            <h3>Reserva ID: {pedido.reserva_id}</h3>
                            <ul>
                                {pedido.trechos.map((trecho, idx) => (
                                    <li key={idx}>
                                        <strong>Origem:</strong> {trecho.origem} |
                                        <strong> Destino:</strong> {trecho.destino} |
                                        <strong> Voo:</strong> {trecho.voo} |
                                        <strong> Assento:</strong> {trecho.assento} |
                                        <strong> Companhia:</strong> {trecho.companhia}
                                    </li>
                                ))}
                            </ul>
                        </li>
                    ))}
                </ul>
            ) : (
                <p>Nenhuma reserva encontrada.</p>
            )}
        </div>
    );
};

export default PedidosUsuario;
