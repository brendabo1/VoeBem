// cliente-react/src/components/Reservar.js
import React, { useState } from 'react';
import { comprarPassagem } from '../api';

const Reservar = ({ user_id, trechos }) => {
    const [assentosSelecionados, setAssentosSelecionados] = useState({});
    const [message, setMessage] = useState('');

    const handleAssentoChange = (voo, assento) => {
        setAssentosSelecionados(prev => ({
            ...prev,
            [voo]: assento
        }));
    };

    const handleReserva = async (e) => {
        e.preventDefault();
        const trechosComAssentos = trechos.map(t => ({
            ...t,
            assento: assentosSelecionados[t.voo]
        }));

        try {
            const mensagem = await comprarPassagem(user_id, trechosComAssentos);
            setMessage(mensagem);
        } catch (error) {
            setMessage(error.message);
        }
    };

    return (
        <div className="container mt-4">
            <h2>Reservar Assentos</h2>
            <form onSubmit={handleReserva}>
                {trechos.map((trecho, index) => (
                    <div key={index} className="form-group">
                        <label>{`Voo: ${trecho.voo} - Assentos Disponíveis`}</label>
                        <select
                            className="form-control"
                            value={assentosSelecionados[trecho.voo] || ''}
                            onChange={(e) => handleAssentoChange(trecho.voo, e.target.value)}
                            required
                        >
                            <option value="" disabled>Selecione um assento</option>
                            {trecho.assentos.map((assento, idx) => (
                                assento.avaliable ? (
                                    <option key={idx} value={assento.cod}>{assento.cod}</option>
                                ) : null
                            ))}
                        </select>
                    </div>
                ))}
                <button type="submit" className="btn btn-primary">Confirmar Reserva</button>
            </form>
            {message && <p className="mt-3">{message}</p>}
        </div>
    );
};

export default Reservar;
