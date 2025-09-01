import { extractFuncionalidad, extractRequerimientoDetalles } from '../utils/dataExtractor';

// URLs base de la intranet (igual que en tu versión Python)
const BASE_URL = 'http://reportes03/reports/report/IyD/Gestion';
const FUNCIONALIDAD_URL = `${BASE_URL}/Funcionalidad`;
const REQUERIMIENTO_URL = `${BASE_URL}/Requerimiento`;

/**
 * Realiza una petición HTTP con manejo de errores
 */
const fetchWithErrorHandling = async (url, options = {}) => {
  try {
    const response = await fetch(url, {
      ...options,
      mode: 'cors', // Permitir CORS para intranet
      credentials: 'include' // Incluir cookies de sesión si es necesario
    });
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    
    return await response.text();
  } catch (error) {
    if (error.name === 'TypeError' && error.message.includes('Failed to fetch')) {
      throw new Error(`No se puede conectar con la intranet (${url}). Verifica que estés en la red corporativa.`);
    }
    throw error;
  }
};

/**
 * Obtiene los datos de funcionalidad desde la intranet
 * Equivalente a la navegación en logic.py
 */
export const fetchFuncionalidadData = async (numeroFuncionalidad) => {
  if (!numeroFuncionalidad || !/^\d+$/.test(numeroFuncionalidad)) {
    throw new Error('Número de funcionalidad inválido. Debe ser numérico.');
  }
  
  // Simular el proceso que hace Selenium:
  // 1. Cargar página principal
  // 2. Llenar input con número de funcionalidad
  // 3. Hacer clic en "Ver informe"
  
  // En una implementación real, esto podría requerir múltiples requests
  // Para simplificar, asumimos que podemos hacer la petición directamente
  const url = `${FUNCIONALIDAD_URL}?Funcionalidad=${numeroFuncionalidad}`;
  
  try {
    console.log(`Intentando acceder a: ${url}`);
    const htmlContent = await fetchWithErrorHandling(url);
    
    // Verificar si la respuesta contiene datos válidos
    if (!htmlContent || htmlContent.length < 100) {
      throw new Error('Respuesta vacía o inválida del servidor de intranet');
    }
    
    console.log(`Respuesta recibida, tamaño: ${htmlContent.length} caracteres`);
    
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
 * Obtiene los datos de un requerimiento específico
 * Equivalente a extraer_requerimiento en requerimientos.py
 */
export const fetchRequerimientoData = async (numeroRequerimiento) => {
  if (!numeroRequerimiento || !/^\d+$/.test(numeroRequerimiento)) {
    throw new Error('Número de requerimiento inválido');
  }
  
  const url = `${REQUERIMIENTO_URL}?TipoRequerimiento=1&Numero=${numeroRequerimiento}`;
  
  try {
    const htmlContent = await fetchWithErrorHandling(url);
    
    if (!htmlContent || htmlContent.length < 100) {
      throw new Error('Respuesta vacía del servidor');
    }
    
    // Extraer datos estructurados del HTML
    const detalles = extractRequerimientoDetalles(htmlContent);
    
    return detalles;
    
  } catch (error) {
    console.error(`Error al obtener requerimiento ${numeroRequerimiento}:`, error);
    throw new Error(`Error al obtener requerimiento ${numeroRequerimiento}: ${error.message}`);
  }
};

/**
 * Valida si se puede conectar con la intranet
 * Útil para verificar conectividad antes de procesar
 */
export const testIntranetConnection = async () => {
  try {
    await fetchWithErrorHandling(FUNCIONALIDAD_URL, {
      method: 'HEAD', // Solo verificar cabeceras
      timeout: 5000
    });
    return true;
  } catch (error) {
    console.warn('No se puede conectar con la intranet:', error.message);
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
