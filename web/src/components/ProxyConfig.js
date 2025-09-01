import React, { useState, useEffect, useCallback } from 'react';
import { setProxyBaseUrl } from '../services/intranetApi';
import './ProxyConfig.css';

const ProxyConfig = () => {
  const [proxyIP, setProxyIP] = useState('');
  const [isConnected, setIsConnected] = useState(false);
  const [isChecking, setIsChecking] = useState(false);

  useEffect(() => {
    // Verificar si ya hay una configuración guardada
    const savedIP = localStorage.getItem('proxyIP');
    if (savedIP) {
      setProxyIP(savedIP);
      checkConnection(savedIP);
    }
  }, [checkConnection]);

  const checkConnection = useCallback(async (ip) => {
    setIsChecking(true);
    try {
      const response = await fetch(`http://${ip}:5000/health`, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
        timeout: 5000
      });
      
      if (response.ok) {
        const data = await response.json();
        if (data.status === 'ok') {
          setIsConnected(true);
          localStorage.setItem('proxyIP', ip);
          setProxyBaseUrl(ip); // Actualizar la configuración global
          return true;
        }
      }
      setIsConnected(false);
      return false;
    } catch (error) {
      console.error('Error conectando al proxy:', error);
      setIsConnected(false);
      return false;
    } finally {
      setIsChecking(false);
    }
  }, []);

  const handleConnect = async () => {
    if (!proxyIP.trim()) {
      alert('Por favor ingresa una IP válida');
      return;
    }
    
    await checkConnection(proxyIP.trim());
  };

  const handleReset = () => {
    localStorage.removeItem('proxyIP');
    setProxyIP('');
    setIsConnected(false);
  };

  if (isConnected) {
    return (
      <div className="proxy-config connected">
        <div className="status-indicator">
          <span className="status-dot connected"></span>
          <span>✅ Conectado al proxy en {proxyIP}:5000</span>
          <button onClick={handleReset} className="btn-reset">🔄 Cambiar</button>
        </div>
      </div>
    );
  }

  return (
    <div className="proxy-config">
      <div className="config-card">
        <h3>🔧 Configuración del Proxy Local</h3>
        <div className="config-content">
          <p>Para usar el generador desde Netlify, necesitas ejecutar el proxy localmente:</p>
          
          <div className="steps">
            <div className="step">
              <span className="step-number">1</span>
              <span>Ejecuta en tu máquina: <code>python proxy_server.py</code></span>
            </div>
            <div className="step">
              <span className="step-number">2</span>
              <span>Busca la línea: <code>"Running on http://192.168.x.x:5000"</code></span>
            </div>
            <div className="step">
              <span className="step-number">3</span>
              <span>Ingresa esa IP aquí:</span>
            </div>
          </div>

          <div className="input-group">
            <input
              type="text"
              value={proxyIP}
              onChange={(e) => setProxyIP(e.target.value)}
              placeholder="192.168.1.100"
              className="ip-input"
              disabled={isChecking}
            />
            <button 
              onClick={handleConnect}
              disabled={isChecking || !proxyIP.trim()}
              className="btn-connect"
            >
              {isChecking ? 'Verificando...' : '🔗 Conectar'}
            </button>
          </div>

          <div className="help-text">
            <p>💡 <strong>Ejemplo:</strong> Si ves "Running on http://192.168.1.105:5000", ingresa: <code>192.168.1.105</code></p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProxyConfig;
