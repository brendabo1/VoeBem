// src/components/Reservar.js
import React, { useState } from 'react';
import { reservarAssentos } from '../api';

const Reservar = () => {
    const [origem, setOrigem] = useState('');
    const [destino, setDestino] = useState('');
    const [assentos, setAssentos] = useState(1);
    const [message, setMessage] = useState('');

    const handleReserva = async (e) => {
        e.preventDefault();
        try {
            await reservarAssentos(origem, destino, assentos);
            setMessage("Reserva realizada com sucesso!");
        } catch (error) {
            setMessage("Erro na reserva. Verifique disponibilidade e tente novamente.");
        }
    };

    return (
        <div className="container">
            <h2>Reservar Assento</h2>
            <form onSubmit={handleReserva}>
                <div className="form-group">
                    <label>Origem</label>
                    <input type="text" className="form-control" value={origem} onChange={(e) => setOrigem(e.target.value)} required />
                </div>
                <div className="form-group">
                    <label>Destino</label>
                    <input type="text" className="form-control" value={destino} onChange={(e) => setDestino(e.target.value)} required />
                </div>
                <div className="form-group">
                    <label>Número de Assentos</label>
                    <input type="number" className="form-control" value={assentos} onChange={(e) => setAssentos(e.target.value)} required />
                </div>
                <button type="submit" className="btn btn-primary">Confirmar Reserva</button>
            </form>
            {message && <p>{message}</p>}
        </div>
    );
};

export default Reservar;
