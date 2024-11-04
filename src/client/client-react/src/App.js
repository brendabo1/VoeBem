// src/App.js
import React, { useState } from 'react';
import Login from './components/Login';
import Supergrafo from './components/Supergrafo';
import Reservar from './components/Reservar';

function App() {
    const [loggedIn, setLoggedIn] = useState(false);

    return (
        <div>
            {!loggedIn ? (
                <Login onLoginSuccess={() => setLoggedIn(true)} />
            ) : (
                <div>
                    <Supergrafo />
                    <Reservar />
                </div>
            )}
        </div>
    );
}

// export default App;


// Exemplo de requisição no App.js
import React, { useEffect, useState } from 'react';

function App() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch(`${process.env.REACT_APP_API_URL}/listar_supergrafo`)
      .then((response) => response.json())
      .then((data) => setData(data));
  }, []);

  return (
    <div>
      <h1>Rotas Disponíveis</h1>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}

export default App;
