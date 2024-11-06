// cliente-react/src/App.js
import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Home from './components/Home';
import Login from './components/Login';
import Menu from './components/Menu';
import Supergrafo from './components/Supergrafo';
import Reservar from './components/Reservar';
import './App.css';

function App() {
    const [loggedIn, setLoggedIn] = useState(false);
    const [userId, setUserId] = useState('');
    const [origem, setOrigem] = useState('');
    const [destino, setDestino] = useState('');
    const [trechosSelecionados, setTrechosSelecionados] = useState([]);

    const handleLoginSuccess = (id) => {
        setLoggedIn(true);
        setUserId(id);
    };

    const handleBuscarRotas = (e) => {
        e.preventDefault();
    };

    return (
        <Router>
            <div>
                <Routes>
                    <Route path="/" element={<Home />} />
                    <Route path="/login" element={<Login onLoginSuccess={handleLoginSuccess} />} />
                    <Route path="/dashboard" element={loggedIn ? <Menu /> : <Navigate to="/login" />} />

                    {/* Rotas para funcionalidades do sistema, acessíveis apenas se logado */}
                    {loggedIn && (
                        <>
                            <Route
                                path="/buscar_rotas"
                                element={
                                    <div className="container mt-4">
                                        <h2>Buscar Rotas</h2>
                                        <form onSubmit={handleBuscarRotas}>
                                            <div className="form-group">
                                                <label>Origem</label>
                                                <input
                                                    type="text"
                                                    className="form-control"
                                                    value={origem}
                                                    onChange={(e) => setOrigem(e.target.value)}
                                                    required
                                                />
                                            </div>
                                            <div className="form-group">
                                                <label>Destino</label>
                                                <input
                                                    type="text"
                                                    className="form-control"
                                                    value={destino}
                                                    onChange={(e) => setDestino(e.target.value)}
                                                    required
                                                />
                                            </div>
                                            <button type="submit" className="btn btn-primary">Buscar Rotas</button>
                                        </form>
                                        <Supergrafo origem={origem} destino={destino} />
                                    </div>
                                }
                            />
                            <Route path="/reservar_assento" element={<Reservar user_id={userId} trechos={trechosSelecionados} />} />
                            <Route path="/supergrafo" element={<Supergrafo />} />
                            <Route path="/meus_pedidos" element={<Supergrafo user_id={userId} />} />
                        </>
                    )}

                    {/* Redirecionamento para login se tentar acessar rota protegida */}
                    <Route path="*" element={<Navigate to={loggedIn ? "/dashboard" : "/login"} />} />
                </Routes>
            </div>
        </Router>
    );
}

export default App;

//     return (
//         <Router>
//             <div>
//                 <Routes>
//                     <Route path="/" element={<Home />} />
//                     <Route path="/login" element={<Login onLoginSuccess={handleLoginSuccess} />} />
//                     <Route path="/dashboard" element={loggedIn ? <Menu /> : <Navigate to="/login" />} />

//                     {loggedIn && (
//                         <>
//                             <Route
//                                 path="/buscar_rotas"
//                                 element={
//                                     <div className="container mt-4">
//                                         <form onSubmit={handleBuscarRotas}>
//                                             <div className="form-group">
//                                                 <label>Origem</label>
//                                                 <input
//                                                     type="text"
//                                                     className="form-control"
//                                                     value={origem}
//                                                     onChange={(e) => setOrigem(e.target.value)}
//                                                     required
//                                                 />
//                                             </div>
//                                             <div className="form-group">
//                                                 <label>Destino</label>
//                                                 <input
//                                                     type="text"
//                                                     className="form-control"
//                                                     value={destino}
//                                                     onChange={(e) => setDestino(e.target.value)}
//                                                     required
//                                                 />
//                                             </div>
//                                             <button type="submit" className="btn btn-primary">Buscar Rotas</button>
//                                         </form>
//                                         <Supergrafo origem={origem} destino={destino} />
//                                     </div>
//                                 }
//                             />
//                             <Route path="/reservar_assento" element={<Reservar user_id={userId} trechos={trechosSelecionados} />} />
//                             <Route path="/ver_supergrafo" element={<Supergrafo origem={origem} destino={destino} />} />
//                             <Route path="/meus_pedidos" element={<Supergrafo user_id={userId} />} />
//                         </>
//                     )}
//                 </Routes>
//             </div>
//         </Router>
//     );
// }

// export default App;
