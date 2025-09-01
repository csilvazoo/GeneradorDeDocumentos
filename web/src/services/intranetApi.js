import { extractFuncionalidad, extractRequerimientoDetalles } from '../utils/dataExtractor';

// URLs del servidor proxy
const PROXY_BASE_URL = 'http://localhost:5000/api';

/**
 * Realiza una petición HTTP con manejo de errores al servidor proxy
 */
const fetchWithErrorHandling = async (url, options = {}) => {
  try {
    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers
      }
    });
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.error || `HTTP ${response.status}: ${response.statusText}`);
    }
    
    return await response.json();
  } catch (error) {
    if (error.name === 'TypeError' && error.message.includes('Failed to fetch')) {
      throw new Error(`No se puede conectar con el servidor proxy (${url}). Verifica que el servidor proxy esté ejecutándose en http://localhost:5000`);
    }
    throw error;
  }
};

/**
 * Obtiene los datos de funcionalidad desde la intranet a través del proxy
 * Equivalente a la navegación en logic.py
 */
export const fetchFuncionalidadData = async (numeroFuncionalidad) => {
  if (!numeroFuncionalidad || !/^\d+$/.test(numeroFuncionalidad)) {
    throw new Error('Número de funcionalidad inválido. Debe ser numérico.');
  }
  
  const url = `${PROXY_BASE_URL}/funcionalidad/${numeroFuncionalidad}`;
  
  try {
    console.log(`Accediendo al proxy: ${url}`);
    const response = await fetchWithErrorHandling(url);
    
    if (!response.success) {
      throw new Error(response.error || 'Respuesta inválida del servidor proxy');
    }
    
    const htmlContent = response.html;
    
    // Verificar si la respuesta contiene datos válidos
    if (!htmlContent || htmlContent.length < 100) {
      throw new Error('Respuesta vacía o inválida del servidor de intranet');
    }
    
    console.log(`Respuesta recibida del proxy, tamaño: ${response.size} caracteres`);
    console.log(`URL original accedida: ${response.url}`);
    
    // También extraer y retornar los datos estructurados
    const funcionalidadInfo = extractFuncionalidad(htmlContent, numeroFuncionalidad);
    
    return {
      html: htmlContent,
      info: funcionalidadInfo
    };
    
  } catch (error) {
    console.error('Error al obtener datos de funcionalidad:', error);
    throw new Error(`Error al obtener funcionalidad ${numeroFuncionalidad}: ${error.message}`);
  }
};

/**
 * Obtiene los datos de un requerimiento específico a través del proxy
 * Equivalente a extraer_requerimiento en requerimientos.py
 */
export const fetchRequerimientoData = async (numeroRequerimiento) => {
  if (!numeroRequerimiento || !/^\d+$/.test(numeroRequerimiento)) {
    throw new Error('Número de requerimiento inválido');
  }
  
  const url = `${PROXY_BASE_URL}/requerimiento/${numeroRequerimiento}`;
  
  try {
    console.log(`Accediendo al proxy para requerimiento: ${url}`);
    const response = await fetchWithErrorHandling(url);
    
    if (!response.success) {
      throw new Error(response.error || 'Respuesta inválida del servidor proxy');
    }
    
    const htmlContent = response.html;
    
    if (!htmlContent || htmlContent.length < 100) {
      throw new Error('Respuesta vacía del servidor');
    }
    
    console.log(`Requerimiento obtenido: ${response.size} caracteres`);
    
    // Extraer datos estructurados del HTML
    const detalles = extractRequerimientoDetalles(htmlContent);
    
    return detalles;
    
  } catch (error) {
    console.error(`Error al obtener requerimiento ${numeroRequerimiento}:`, error);
    throw new Error(`Error al obtener requerimiento ${numeroRequerimiento}: ${error.message}`);
  }
};

/**
 * Valida si se puede conectar con el servidor proxy
 * Útil para verificar conectividad antes de procesar
 */
export const testIntranetConnection = async () => {
  try {
    const response = await fetchWithErrorHandling(`${PROXY_BASE_URL}/../health`);
    return response.status === 'ok';
  } catch (error) {
    console.warn('No se puede conectar con el servidor proxy:', error.message);
    return false;
  }
};

/**
 * Obtiene múltiples requerimientos en paralelo (con limitación)
 * Para evitar sobrecargar el servidor de intranet
 */
export const fetchMultipleRequerimientos = async (numerosRequerimientos, maxConcurrent = 3) => {
  const results = [];
  const errors = [];
  
  // Procesar en lotes para no sobrecargar el servidor
  for (let i = 0; i < numerosRequerimientos.length; i += maxConcurrent) {
    const batch = numerosRequerimientos.slice(i, i + maxConcurrent);
    
    const batchPromises = batch.map(async (numero) => {
      try {
        const data = await fetchRequerimientoData(numero);
        return { numero, data, success: true };
      } catch (error) {
        return { numero, error: error.message, success: false };
      }
    });
    
    const batchResults = await Promise.all(batchPromises);
    
    batchResults.forEach(result => {
      if (result.success) {
        results.push(result);
      } else {
        errors.push(result);
      }
    });
    
    // Pequeña pausa entre lotes para ser respetuosos con el servidor
    if (i + maxConcurrent < numerosRequerimientos.length) {
      await new Promise(resolve => setTimeout(resolve, 1000));
    }
  }
  
  return { results, errors };
};
