// cliente-react/src/components/CompraAssento.js
// import React, { useEffect, useState } from 'react';
// import { useLocation, useNavigate } from 'react-router-dom';
// import { verificarAssentos, confirmarCompra } from '../api';

// const CompraAssento = () => {
//     const location = useLocation();
//     const rotaSelecionada = location.state?.rotaSelecionada;

    // useEffect(() => {
    //     const fetchAssentosDisponiveis = async () => {
    //         try {
    //             const response = await verificarAssentos(rotaSelecionada);
    //             setAssentosDisponiveis(response);
    //         } catch (err) {
    //             console.error("Erro ao buscar assentos:", err);
    //         }
    //     };

    //     fetchAssentosDisponiveis();
    // }, [rotaSelecionada]);

    // const handleSelecionarAssento = (vooId, assento) => {
    //     setAssentosSelecionados(prev => ({ ...prev, [vooId]: assento }));
    // };

    // const handleConfirmarCompra = async () => {
    //     try {
    //         await confirmarCompra(assentosSelecionados);
    //         alert("Compra confirmada com sucesso!");
    //         navigate("/"); // Volta para a tela inicial
    //     } catch (err) {
    //         console.error("Erro ao confirmar compra:", err);
    //         alert("Erro ao confirmar compra. Tente novamente.");
    //     }
    // };

    // Função para formatar a duração em horas e minutos
//     const formatarDuracao = (minutos) => {
//         const horas = Math.floor(minutos / 60);
//         const mins = minutos % 60;
//         return `${horas}h ${mins}m`;
//     };

//     if (!rotaSelecionada) {
//         return <p>Nenhuma rota selecionada. Retorne à página de busca para selecionar uma rota.</p>;
//     }
//     return (
//         <div>
//             <h2>Detalhes da Rota Selecionada para Compra</h2>
//             <ul>
//                 {rotaSelecionada.map((voo, index) => (
//                     <li key={index}>
//                         <strong>Origem:</strong> {voo.origem} |
//                         <strong> Voo:</strong> {voo.voo} |
//                         <strong> Conexão para:</strong> {voo.destino} |
//                         <strong> Duração:</strong> {formatarDuracao(voo.duracao)} |
//                         <strong> Companhia:</strong> {voo.companhia}
//                     </li>
//                 ))}
//             </ul>
//             <button type="button" className="btn btn-primary">
//                 Confirmar Compra
//             </button>
//         </div>
//     );
// };

// export default CompraAssento;
//     return (
//         <div>
//             <h2>Seleção de Assentos</h2>
//             {assentosDisponiveis.length > 0 ? (
//                 <ul>
//                     {assentosDisponiveis.map((voo, index) => (
//                         <li key={index}>
//                             <h3>Voo: {voo.voo}</h3>
//                             <p>Origem: {voo.origem} | Destino: {voo.destino}</p>
//                             <p>Assentos Disponíveis:</p>
//                             <ul>
//                                 {voo.assentos.map((assento) => (
//                                     <li key={assento}>
//                                         <button 
//                                             onClick={() => handleSelecionarAssento(voo.voo, assento)}
//                                             disabled={assentosSelecionados[voo.voo] === assento}
//                                         >
//                                             {assento}
//                                         </button>
//                                     </li>
//                                 ))}
//                             </ul>
//                         </li>
//                     ))}
//                 </ul>
//             ) : (
//                 <p>Carregando assentos disponíveis...</p>
//             )}
//             <button onClick={handleConfirmarCompra} disabled={Object.keys(assentosSelecionados).length !== rotaSelecionada.length}>
//                 Confirmar Compra
//             </button>
//         </div>
//     );
// };

//export default CompraAssento;
