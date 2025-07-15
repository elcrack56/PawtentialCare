import React, { useState, useEffect, useCallback } from 'react';
import './App.css';

const API_URL = 'http://localhost:8000';

function App() {
  const [users, setUsers] = useState([]);
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');

  const fetchUsers = useCallback(async () => {
    try {
      console.log("Funcionalidad para obtener todos los usuarios pendiente de implementar en el backend.");
    } catch (error) {
      console.error("Error fetching users:", error);
    }
  }, []);

  useEffect(() => {
    fetchUsers();
  }, [fetchUsers]);

  const handleCreateUser = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(`${API_URL}/api/users`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ full_name: fullName, email: email }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Error al crear el usuario');
      }

      const newUser = await response.json();
      setUsers([...users, newUser]); 
      setFullName('');
      setEmail('');
      alert(`Usuario "${newUser.full_name}" creado con éxito!`);
      fetchUsers(); 
    } catch (error) {
      console.error("Error creating user:", error);
      alert(error.message);
    }
  };

  return (
    <div className="container">
      <header>
        <h1>🐾 PawtentialCare</h1>
        <p>El mejor cuidado para tus mascotas</p>
      </header>

      <main>
        <div className="card">
          <h2>Crear Nuevo Usuario</h2>
          <form onSubmit={handleCreateUser}>
            <div className="form-group">
              <label htmlFor="fullName">Nombre Completo:</label>
              <input
                type="text"
                id="fullName"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                placeholder="Ej: Ada Lovelace"
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="email">Correo Electrónico:</label>
              <input
                type="email"
                id="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Ej: ada@example.com"
                required
              />
            </div>
            <button type="submit" className="btn-primary">Registrar Usuario</button>
          </form>
        </div>

        <div className="card">
          <h2>Usuarios Registrados</h2>
          {/* Aquí se mostraría la lista de usuarios cuando el endpoint GET esté listo */}
          <p>(La lista de usuarios aparecerá aquí una vez implementado el endpoint)</p>
          <ul>
            {users.map(user => (
              <li key={user.id}>{user.full_name} ({user.email})</li>
            ))}
          </ul>
        </div>
      </main>
    </div>
  );
}

export default App;