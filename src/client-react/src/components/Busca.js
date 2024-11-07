// cliente-react/src/components/BuscaRota.js
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { buscarRotas } from '../api';

const BuscaRotas = () => {
    const [origem, setOrigem] = useState('');
    const [destino, setDestino] = useState('');
    const [rotas, setRotas] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [rotaSelecionada, setRotaSelecionada] = useState(null);
    const navigate = useNavigate();

    const handleBuscarRotas = async (e) => {
        e.preventDefault();
        setLoading(true); // Exibir barra de carregamento
        setError(null);
        setRotas([]);

        try {
            const rotasEncontradas = await buscarRotas(origem, destino);
            console.log(rotasEncontradas)
            if (Array.isArray(rotasEncontradas) && rotasEncontradas.length > 0) {
                setRotas(rotasEncontradas);
            } else {
                setError("Nenhuma rota encontrada.");
            }
        } catch (err) {
            console.error("Erro ao buscar rotas:", err);
            setError("Erro ao buscar rotas. Tente novamente.");
        }finally {
            setLoading(false); // Ocultar barra de carregamento
        }
    };

    const handleSelecionarRota = async (rota) => {
        try {
            setLoading(true);
            
            //const response = await verificarAssentos(rotaSelecionada);
            alert("Rota selecionada com sucesso!");
            setRotaSelecionada(rota);
            console.log(rota);
            setRotaSelecionada(rota);
            navigate("/selec_assento", { state: { rotaSelecionada: rota } });
        } catch (err) {
            console.error("Erro ao enviar a rota selecionada:", err);
            setError("Erro ao processar a compra. Tente novamente.");
        } finally {
            setLoading(false);
        }
    };


    // Função para formatar a duração em horas e minutos
    const formatarDuracao = (minutos) => {
        const horas = Math.floor(minutos / 60);
        const mins = minutos % 60;
        return `${horas}h ${mins}m`;
    };


    return (
        <div>
            <h2>Buscar Rotas</h2>
            <form onSubmit={handleBuscarRotas}>
                <div className="form-box">
                <label>Origem:</label>
                <input type="text" value={origem} onChange={(e) => setOrigem(e.target.value)} required />
                </div>
                <div className="form-box">
                <label>Destino:</label>
                <input type="text" value={destino} onChange={(e) => setDestino(e.target.value)} required />
                </div>
                <button type="submit" className="btn btn-primary"> Buscar Rotas</button>
            </form>
            {error && <p>{error}</p>}
            {loading && <p>Carregando...</p>}
            {rotas.length > 0 && (
                <ul>
                    {rotas.map((rota, index) => (
                        <li key={index}>
                            <h3>Rota {index + 1}</h3>
                            <ul>
                                {rota.map((voo, vooIndex) => (
                                    <li key={vooIndex}>
                                        <strong>Origem:</strong> {voo.origem} | 
                                        <strong> Voo:</strong> {voo.voo} | 
                                        <strong> Conexão para:</strong> {voo.destino} | 
                                        <strong> Duração:</strong> {formatarDuracao(voo.duracao)} | 
                                        <strong> Companhia:</strong> {voo.companhia}
                                    </li>
                                ))}
                            </ul>
                            <button type="submit" className="btn btn-primary" onClick={() => handleSelecionarRota(rota)}>
                                Selecionar
                            </button>
                        </li>
                    ))}
                </ul>
            )}
            {rotaSelecionada && (
                <div>
                    <h3>Rota Selecionada:</h3>
                    <ul>
                        {rotaSelecionada.map((voo, index) => (
                            <li key={index}>
                                <strong>Voo:</strong> {voo.voo} | 
                                <strong> Conexão para:</strong> {voo.next_dest} | 
                                <strong> Duração:</strong> {formatarDuracao(voo.duracao)} | 
                                <strong> Companhia:</strong> {voo.companhia}
                            </li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
};

export default BuscaRotas;