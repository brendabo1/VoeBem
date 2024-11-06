// cliente-react/src/components/Supergrafo.js
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './Supergrafo.css'; // Arquivo CSS para estilizar o componente

function Supergrafo() {
    const [supergrafo, setSupergrafo] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    // Função para buscar o supergrafo do backend
    const fetchSupergrafo = async () => {
        try {
            const response = await axios.get('http://localhost:5000/supergrafo');
            if (response.status === 200) {
                const grafo = response.data.supergrafo;
                const formattedGrafo = formatSupergrafo(grafo);
                setSupergrafo(formattedGrafo);
            } else {
                setError("Erro ao carregar o supergrafo.");
            }
        } catch (err) {
            console.error("Erro ao buscar o supergrafo:", err);
            setError("Erro de conexão com o servidor.");
        } finally {
            setLoading(false);
        }
    };

    // Formatação do supergrafo para uma estrutura fácil de exibir
    const formatSupergrafo = (grafo) => {
        const formatted = [];
        for (const origem in grafo) {
            for (const destino in grafo[origem]) {
                grafo[origem][destino].forEach((voo) => {
                    formatted.push({
                        origem,
                        destino,
                        vooId: voo.voo,
                        duracao: voo.duracao,
                        companhia: voo.companhia,
                    });
                });
            }
        }
        return formatted;
    };

    useEffect(() => {
        fetchSupergrafo();
    }, []);

    if (loading) return <p>Carregando supergrafo...</p>;
    if (error) return <p>{error}</p>;

    return (
        <div className="supergrafo-container">
            <h2>Rotas Disponíveis</h2>
            <table className="supergrafo-table">
                <thead>
                    <tr>
                        <th>Origem</th>
                        <th>Destino</th>
                        <th>Voo ID</th>
                        <th>Duração</th>
                        <th>Companhia</th>
                    </tr>
                </thead>
                <tbody>
                    {supergrafo.map((rota, index) => (
                        <tr key={index}>
                            <td>{rota.origem}</td>
                            <td>{rota.destino}</td>
                            <td>{rota.vooId}</td>
                            <td>{rota.duracao}</td>
                            <td>{rota.companhia}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

export default Supergrafo;


// import React, { useEffect, useState } from 'react';
// import axios from 'axios';

// function Supergrafo() {
//     const [supergrafo, setSupergrafo] = useState([]);
//     const [loading, setLoading] = useState(true);
//     const [error, setError] = useState(null);

//     // Função para buscar o supergrafo do backend
//     const fetchSupergrafo = async () => {
//         try {
//             const response = await axios.get('http://localhost:5000/supergrafo');
//             if (response.status === 200) {
//                 const grafo = response.data.supergrafo;
//                 const formattedGrafo = formatSupergrafo(grafo);
//                 setSupergrafo(formattedGrafo);
//             } else {
//                 setError("Erro ao carregar o supergrafo.");
//             }
//         } catch (err) {
//             console.error("Erro ao buscar o supergrafo:", err);
//             setError("Erro de conexão com o servidor.");
//         } finally {
//             setLoading(false);
//         }
//     };

//     // Formatação do supergrafo para uma estrutura fácil de exibir
//     const formatSupergrafo = (grafo) => {
//         const formatted = [];
//         for (const origem in grafo) {
//             for (const destino in grafo[origem]) {
//                 grafo[origem][destino].forEach((voo) => {
//                     formatted.push({
//                         origem,
//                         destino,
//                         vooId: voo.voo,
//                         duracao: voo.duracao,
//                         companhia: voo.companhia,
//                     });
//                 });
//             }
//         }
//         return formatted;
//     };

//     useEffect(() => {
//         fetchSupergrafo();
//     }, []);

//     if (loading) return <p>Carregando supergrafo...</p>;
//     if (error) return <p>{error}</p>;

//     return (
//         <div className="supergrafo-container">
//             <h2>Rotas Disponíveis</h2>
//             <ul>
//                 {supergrafo.map((rota, index) => (
//                     <li key={index} className="supergrafo-item">
//                         <strong>Origem:</strong> {rota.origem} | 
//                         <strong> Destino:</strong> {rota.destino} | 
//                         <strong> Voo ID:</strong> {rota.vooId} | 
//                         <strong> Duração:</strong> {rota.duracao} horas | 
//                         <strong> Companhia:</strong> {rota.companhia}
//                     </li>
//                 ))}
//             </ul>
//         </div>
//     );
// }

// export default Supergrafo;
