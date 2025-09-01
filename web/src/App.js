import React, { useState } from 'react';
import './App.css';
import DocumentGenerator from './components/DocumentGenerator';

function App() {
  return (
    <div className="App">
      <header className="app-header">
        <div className="container">
          <h1>🔧 Generador de Documentos Funcionales</h1>
          <p className="subtitle">Versión Web - Automatización de documentos AFU2505</p>
        </div>
      </header>
      
      <main className="container">
        <DocumentGenerator />
      </main>
      
      <footer className="app-footer">
        <div className="container">
          <p>&copy; 2025 - Generador de Documentos Funcionales v2.0</p>
        </div>
      </footer>
    </div>
  );
}

export default App;
