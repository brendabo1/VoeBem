// src/components/Supergrafo.js
import React, { useEffect, useState } from 'react';
import { listarSupergrafo } from '../api';

const Supergrafo = () => {
    const [supergrafo, setSupergrafo] = useState({});

    useEffect(() => {
        const fetchSupergrafo = async () => {
            const response = await listarSupergrafo();
            setSupergrafo(response.data);
        };
        fetchSupergrafo();
    }, []);

    return (
        <div className="container">
            <h2>Supergrafo de Rotas</h2>
            <table className="table">
                <thead>
                    <tr>
                        <th>Origem</th>
                        <th>Destino</th>
                        <th>Detalhes</th>
                    </tr>
                </thead>
                <tbody>
                    {Object.entries(supergrafo).map(([origem, destinos]) =>
                        Object.entries(destinos).map(([destino, detalhes]) => (
                            <tr key={`${origem}-${destino}`}>
                                <td>{origem}</td>
                                <td>{destino}</td>
                                <td>{JSON.stringify(detalhes)}</td>
                            </tr>
                        ))
                    )}
                </tbody>
            </table>
        </div>
    );
};

export default Supergrafo;
