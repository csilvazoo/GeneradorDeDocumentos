import React, { useState } from 'react';
import { extractRequerimientos } from '../utils/dataExtractor';
import { generateWordDocument } from '../services/documentGenerator';
import { fetchFuncionalidadData, fetchRequerimientoData } from '../services/intranetApi';
import './DocumentGenerator.css';

const DocumentGenerator = () => {
  const [numeroFuncionalidad, setNumeroFuncionalidad] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [logs, setLogs] = useState([]);
  const [requerimientos, setRequerimientos] = useState([]);
  const [error, setError] = useState('');

  const addLog = (message) => {
    setLogs(prev => [...prev, `${new Date().toLocaleTimeString()}: ${message}`]);
  };

  const clearLogs = () => {
    setLogs([]);
    setError('');
    setRequerimientos([]);
  };

  const validateNumeroFuncionalidad = (numero) => {
    return /^\d+$/.test(numero) && numero.length > 0;
  };

  const generarDocumento = async () => {
    if (!validateNumeroFuncionalidad(numeroFuncionalidad)) {
      setError('Número de funcionalidad inválido. Debe ser numérico.');
      return;
    }

    setIsGenerating(true);
    setError('');
    clearLogs();

    try {
      addLog('🚀 Iniciando proceso de generación...');
      
      // 1. Obtener datos de funcionalidad
      addLog('📊 Obteniendo datos de funcionalidad de la intranet...');
      const funcionalidadData = await fetchFuncionalidadData(numeroFuncionalidad);
      addLog('✅ Datos de funcionalidad obtenidos correctamente');

      // 2. Extraer requerimientos
      addLog('🔍 Analizando requerimientos asociados...');
      const requerimientosEncontrados = extractRequerimientos(funcionalidadData);
      setRequerimientos(requerimientosEncontrados);
      
      if (requerimientosEncontrados.length === 0) {
        addLog('⚠️  No se encontraron requerimientos para esta funcionalidad');
        setError('No existe funcionalidad o no tiene requerimientos asociados.');
        return;
      }

      addLog(`📋 Requerimientos encontrados:`);
      // Mostrar en dos columnas como en la versión desktop
      const half = Math.ceil(requerimientosEncontrados.length / 2);
      for (let i = 0; i < half; i++) {
        const left = `  ${i + 1}. ${requerimientosEncontrados[i]}`;
        const rightIdx = i + half;
        if (rightIdx < requerimientosEncontrados.length) {
          const right = `  ${rightIdx + 1}. ${requerimientosEncontrados[rightIdx]}`;
          addLog(`${left.padEnd(25)} ${right}`);
        } else {
          addLog(left);
        }
      }

      // 3. Obtener detalles de cada requerimiento
      addLog('📝 Obteniendo detalles de cada requerimiento...');
      const requerimientosDetallados = [];
      
      for (let i = 0; i < requerimientosEncontrados.length; i++) {
        const nro = requerimientosEncontrados[i];
        addLog(`   📄 Procesando requerimiento ${nro}...`);
        
        try {
          const detalles = await fetchRequerimientoData(nro);
          requerimientosDetallados.push({
            numero: nro,
            ...detalles
          });
          addLog(`   ✅ Requerimiento ${nro} procesado`);
        } catch (reqError) {
          addLog(`   ⚠️  Error al procesar requerimiento ${nro}: ${reqError.message}`);
          // Continuar con valores por defecto
          requerimientosDetallados.push({
            numero: nro,
            fechaAlta: 'no hay',
            titulo: 'no hay',
            necesidad: 'no hay',
            implementacion: 'no hay',
            cliente: 'no hay',
            relevamientos: 'no hay',
            documento: 'no hay',
            documentoLink: '',
            incidente: '',
            incidenteLink: ''
          });
        }
      }

      // 4. Generar documento Word
      addLog('📄 Generando documento Word...');
      const documento = await generateWordDocument(
        numeroFuncionalidad,
        funcionalidadData,
        requerimientosDetallados
      );

      // 5. Descargar documento
      addLog('💾 Descargando documento...');
      const blob = new Blob([documento], { 
        type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' 
      });
      
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `AFU2505_Funcionalidad_${numeroFuncionalidad}.docx`;
      link.click();
      window.URL.revokeObjectURL(url);

      addLog('🎉 ¡Proceso completado exitosamente!');
      addLog('📁 Documento descargado en tu carpeta de descargas');

    } catch (error) {
      console.error('Error durante la generación:', error);
      setError(`Error durante la generación: ${error.message}`);
      addLog(`❌ Error: ${error.message}`);
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="document-generator">
      <div className="card">
        <h2>🔧 Generar Nuevo Documento</h2>
        
        <div className="form-group">
          <label htmlFor="numeroFunc">Número de Funcionalidad:</label>
          <input
            id="numeroFunc"
            type="text"
            className="form-control"
            value={numeroFuncionalidad}
            onChange={(e) => setNumeroFuncionalidad(e.target.value)}
            placeholder="Ej: 12345"
            disabled={isGenerating}
          />
        </div>

        <button
          className={`btn btn-primary ${isGenerating ? 'generating' : ''}`}
          onClick={generarDocumento}
          disabled={isGenerating || !numeroFuncionalidad}
        >
          {isGenerating && <span className="loading-spinner"></span>}
          {isGenerating ? 'Generando Documento...' : '🚀 Generar Documento'}
        </button>

        {error && (
          <div className="error">
            ❌ {error}
          </div>
        )}
      </div>

      {logs.length > 0 && (
        <div className="card">
          <h3>📋 Registro de Proceso</h3>
          <div className="logs-container">
            {logs.map((log, index) => (
              <div key={index} className="log-entry">
                {log}
              </div>
            ))}
          </div>
          <button 
            className="btn btn-secondary" 
            onClick={clearLogs}
            style={{ marginTop: '1rem' }}
          >
            🗑️ Limpiar Logs
          </button>
        </div>
      )}

      {requerimientos.length > 0 && (
        <div className="card">
          <h3>📊 Requerimientos Detectados ({requerimientos.length})</h3>
          <div className="requirements-grid">
            {requerimientos.map((req, index) => (
              <div key={index} className="requirement-item">
                <strong>#{index + 1}</strong> - Requerimiento {req}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default DocumentGenerator;
