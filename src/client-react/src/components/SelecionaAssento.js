// cliente-react/src/components/SelecionaAssento.js
import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { realizarCompra } from '../api';
import './SelecionaAssento.css';

const SelecionaAssento = () => {
    const location = useLocation();
    const navigate = useNavigate();
    const rotaSelecionada = location.state?.rotaSelecionada || [];
    const [assentosSelecionados, setAssentosSelecionados] = useState({});
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleSelecionarAssento = (vooIndex, assento) => {
        setAssentosSelecionados((prevState) => ({
            ...prevState,
            [vooIndex]: assento,
        }));
    };

    const handleConfirmarCompra = async () => {
        setLoading(true);
        setError(null);

         // Montar a lista de trechos com origem, destino, voo, assento e companhia
         const listaDeTrechos = rotaSelecionada.map((voo, index) => ({
            origem: voo.origem,
            destino: voo.destino,
            voo: voo.voo,
            assento: assentosSelecionados[index],
            companhia: voo.companhia,
        }));

        try {
            const userId = localStorage.getItem('userId');
            console.log(listaDeTrechos, userId)
            await realizarCompra(listaDeTrechos, userId);
            console.log(listaDeTrechos)
            //await realizarCompra({trechos: listaDeTrechos, userId});
            navigate('/compra');
            
        } catch (err) {
            console.error('Erro ao realizar compra:', err);
            setError('Erro ao realizar a compra. Tente novamente.');
        } finally {
            setLoading(false);
        }
    };

    const formatarDuracao = (minutos) => {
        const horas = Math.floor(minutos / 60);
        const mins = minutos % 60;
        return `${horas}h ${mins}m`;
    };

    return (
        <div>
            <h2>Selecionar Assentos</h2>
            {error && <p>{error}</p>}
            {rotaSelecionada.map((voo, index) => (
                <div key={index} className="voo-box">
                    <h3>Voo {voo.voo} - {voo.origem} para {voo.destino}</h3>
                    <p><strong>Companhia:</strong> {voo.companhia}</p>
                    <p><strong>Duração:</strong> {formatarDuracao(voo.duracao)}</p>
                    <p><strong>Assentos Disponíveis:</strong></p>
                    <div className="assentos-disponiveis">
                        {voo.assentos_disponiveis.map((assento, idx) => (
                            <button
                                key={idx}
                                onClick={() => handleSelecionarAssento(index, assento)}
                                className={`assento ${assentosSelecionados[index] === assento ? 'selecionado' : ''}`}
                            >
                                {assento}
                            </button>
                        ))}
                    </div>
                </div>
            ))}
            <button
                onClick={handleConfirmarCompra}
                disabled={Object.keys(assentosSelecionados).length !== rotaSelecionada.length}
                className="btn btn-primary"
            >
                Confirmar Compra
            </button>
            {loading && <p>Processando compra...</p>}
        </div>
    );
};

export default SelecionaAssento;
