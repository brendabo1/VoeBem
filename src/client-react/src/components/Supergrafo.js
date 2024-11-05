// cliente-react/src/components/Supergrafo.js
import React, { useEffect, useState } from 'react';
import { buscarRotas } from '../api';

const Supergrafo = ({ origem, destino }) => {
    const [rotas, setRotas] = useState([]);
    const [error, setError] = useState('');

    useEffect(() => {
        const fetchRotas = async () => {
            try {
                const rotasEncontradas = await buscarRotas(origem, destino);
                setRotas(rotasEncontradas);
            } catch (err) {
                setError(err.message);
            }
        };
        fetchRotas();
    }, [origem, destino]);

    return (
        <div className="container">
            <h2>Rotas Disponíveis</h2>
            {error && <p className="text-danger">{error}</p>}
            {rotas.length > 0 ? (
                <ul className="list-group">
                    {rotas.map((rota, index) => (
                        <li key={index} className="list-group-item">
                            <strong>Voo:</strong> {rota.voo} | <strong>Duração:</strong> {rota.duracao} | <strong>Servidor:</strong> {rota.servidor}
                        </li>
                    ))}
                </ul>
            ) : (
                <p>Nenhuma rota encontrada.</p>
            )}
        </div>
    );
};

export default Supergrafo;
