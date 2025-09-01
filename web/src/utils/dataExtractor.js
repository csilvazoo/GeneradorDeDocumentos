/**
 * Extrae los números de requerimientos del HTML de la funcionalidad
 * Adaptado de la lógica Python en logic.py
 */
export const extractRequerimientos = (htmlContent) => {
  const parser = new DOMParser();
  const doc = parser.parseFromString(htmlContent, 'text/html');
  
  // Buscar divs con los estilos específicos (adaptado del XPath Python)
  const divs = doc.querySelectorAll(`
    div[style*="width:20.22mm;min-width: 20.22mm;"],
    div[style*="width:23.24mm;min-width: 23.24mm;"]
  `);
  
  const requerimientoNros = [];
  let afterReqCliente = false;
  
  divs.forEach(div => {
    const text = div.textContent.trim();
    
    if (text === "Req. Cliente") {
      afterReqCliente = true;
      return;
    }
    
    if (afterReqCliente) {
      if (/^\d+$/.test(text)) {
        // Filtrar por rango de números para distinguir requerimientos de incidentes
        // Requerimientos válidos: 99-99999
        // Incidentes: 100000+
        const num = parseInt(text);
        if (num >= 99 && num <= 99999) {
          requerimientoNros.push(text);
        }
      } else if (text === "Req. Cliente") {
        // Continuar si encuentra otro "Req. Cliente"
        return;
      }
    }
  });
  
  return requerimientoNros;
};

/**
 * Extrae los datos de funcionalidad del HTML
 * Adaptado de funcionalidad.py
 */
export const extractFuncionalidad = (htmlContent, numeroFuncionalidad) => {
  const parser = new DOMParser();
  const doc = parser.parseFromString(htmlContent, 'text/html');
  
  const campos = {
    'Funcionalidad nro.': numeroFuncionalidad,
    'Nombre': '',
    'Descripción': '',
    'Producto': '',
    'Equipo': '',
    'Fecha alta': ''
  };
  
  // Buscar todas las filas de tabla
  const rows = doc.querySelectorAll('tr');
  
  rows.forEach(row => {
    const cells = row.querySelectorAll('td, th');
    if (cells.length >= 2) {
      const label = cells[0].textContent.trim().toLowerCase();
      const valor = cells[1].textContent.trim();
      
      if (label.includes('nombre')) {
        campos['Nombre'] = valor;
      } else if (label.includes('descripci') || label.includes('descrip')) {
        campos['Descripción'] = valor;
      } else if (label.includes('producto')) {
        campos['Producto'] = valor;
      } else if (label.includes('equipo')) {
        campos['Equipo'] = valor;
      } else if (label.includes('fecha alta')) {
        campos['Fecha alta'] = valor;
      }
    }
  });
  
  // Establecer valores por defecto si están vacíos
  Object.keys(campos).forEach(key => {
    if (!campos[key] && key !== 'Funcionalidad nro.') {
      campos[key] = 'no hay';
    }
  });
  
  return campos;
};

/**
 * Extrae los datos de un requerimiento del HTML
 * Adaptado de requerimientos.py
 */
export const extractRequerimientoDetalles = (htmlContent) => {
  const parser = new DOMParser();
  const doc = parser.parseFromString(htmlContent, 'text/html');
  
  const campos = {
    fechaAlta: '',
    titulo: '',
    necesidad: '',
    implementacion: '',
    cliente: '',
    relevamientos: '',
    documento: '',
    documentoLink: '',
    incidente: '',
    incidenteLink: ''
  };
  
  // Buscar todas las filas de tabla
  const rows = doc.querySelectorAll('tr');
  
  rows.forEach(row => {
    const cells = row.querySelectorAll('td, th');
    if (cells.length >= 2) {
      const label = cells[0].textContent.trim().toLowerCase();
      const valor = cells[1].textContent.trim();
      
      if (label.includes('fecha alta')) {
        campos.fechaAlta = valor;
      } else if (label.includes('nombre')) {
        campos.titulo = valor;
      } else if (label.includes('necesidad')) {
        campos.necesidad = valor;
      } else if (label.includes('implem. sugerida') || label.includes('implementación')) {
        campos.implementacion = valor;
      } else if (label.includes('cliente')) {
        campos.cliente = valor;
      } else if (label.includes('requerido por')) {
        campos.relevamientos = valor;
      } else if (label === 'documento') {
        // Extraer número de documento
        const docNumMatch = valor.match(/(\d+)/);
        if (docNumMatch) {
          campos.documento = docNumMatch[1];
        }
        
        // Extraer link de documento
        const linkElement = cells[1].querySelector('a[href]');
        if (linkElement) {
          const href = linkElement.getAttribute('href');
          const jsMatch = href.match(/window\.open\('([^']+)'/);
          if (jsMatch) {
            campos.documentoLink = jsMatch[1];
          } else {
            campos.documentoLink = href;
          }
        }
      }
    }
  });
  
  // Buscar incidentes (números de 6+ dígitos)
  const incidenteLinks = doc.querySelectorAll('a[href]');
  incidenteLinks.forEach(link => {
    const text = link.textContent.trim();
    if (/^\d{6,}$/.test(text)) {
      // Verificar que sea realmente un incidente (100000+)
      const num = parseInt(text);
      if (num >= 100000) {
        campos.incidente = text;
        const href = link.getAttribute('href');
        const jsMatch = href.match(/window\.open\('([^']+)'/);
        if (jsMatch) {
          campos.incidenteLink = jsMatch[1];
        } else {
          campos.incidenteLink = href;
        }
      }
    }
  });
  
  // Procesar cliente (formato "número - descripción")
  if (campos.cliente) {
    const clienteMatch = campos.cliente.match(/(\d+)(.*)/);
    if (clienteMatch) {
      const nroCliente = clienteMatch[1].trim();
      const desc = clienteMatch[2].trim();
      if (desc) {
        campos.cliente = `${nroCliente} - ${desc}`;
      } else {
        campos.cliente = nroCliente;
      }
    }
  }
  
  // Establecer valores por defecto
  if (campos.documento) {
    campos.relevamientos = '';
  } else {
    campos.relevamientos = 'no hay';
    campos.documento = 'no hay';
    campos.documentoLink = '';
  }
  
  ['fechaAlta', 'titulo', 'necesidad', 'implementacion', 'cliente'].forEach(key => {
    if (!campos[key]) {
      campos[key] = 'no hay';
    }
  });
  
  return campos;
};
