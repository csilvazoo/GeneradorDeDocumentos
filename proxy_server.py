"""
Servidor Proxy para el Generador de Documentos Funcionales
Este servidor actúa como intermediario entre la aplicación web y la intranet corporativa
para evitar problemas de CORS.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from requests_ntlm import HttpNtlmAuth
from urllib.parse import urljoin
import logging
import sys
import os

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Permitir todas las peticiones CORS

# URLs base de la intranet
BASE_URL = 'http://reportes03/reports/report/IyD/Gestion'
FUNCIONALIDAD_URL = f'{BASE_URL}/Funcionalidad'
REQUERIMIENTO_URL = f'{BASE_URL}/Requerimiento'

def get_auth_session():
    """Crear sesión con autenticación automática de Windows (NTLM)"""
    session = requests.Session()
    
    # Usar autenticación NTLM automática con las credenciales del usuario actual de Windows
    # Esto equivale a usar las mismas credenciales que usa el navegador automáticamente
    session.auth = HttpNtlmAuth('', '')  # Credenciales vacías = usar usuario actual de Windows
    
    logger.info("Usando autenticación automática de Windows (NTLM)")
    return session

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint para verificar que el servidor está funcionando"""
    return jsonify({'status': 'ok', 'message': 'Proxy server is running'})

@app.route('/api/funcionalidad/<numero>', methods=['GET'])
def get_funcionalidad(numero):
    """
    Obtiene los datos de una funcionalidad desde la intranet
    """
    try:
        # Validar que el número sea válido
        if not numero.isdigit():
            return jsonify({'error': 'Número de funcionalidad inválido'}), 400
        
        # Construir la URL
        url = f'{FUNCIONALIDAD_URL}?Funcionalidad={numero}'
        logger.info(f'Accediendo a: {url}')
        
        # Crear sesión con autenticación
        session = get_auth_session()
        
        # Hacer la petición a la intranet
        response = session.get(url, timeout=30)
        response.raise_for_status()
        
        # Verificar que la respuesta tenga contenido
        if not response.text or len(response.text) < 100:
            return jsonify({'error': 'Respuesta vacía o inválida del servidor'}), 500
        
        logger.info(f'Respuesta recibida: {len(response.text)} caracteres')
        
        return jsonify({
            'success': True,
            'html': response.text,
            'url': url,
            'size': len(response.text)
        })
        
    except requests.exceptions.Timeout:
        error_msg = f'Timeout al acceder a funcionalidad {numero}'
        logger.error(error_msg)
        return jsonify({'error': error_msg}), 408
        
    except requests.exceptions.ConnectionError:
        error_msg = f'No se puede conectar con la intranet. Verifica la red corporativa.'
        logger.error(error_msg)
        return jsonify({'error': error_msg}), 503
        
    except requests.exceptions.HTTPError as e:
        error_msg = f'Error HTTP {e.response.status_code}: {e.response.reason}'
        logger.error(error_msg)
        return jsonify({'error': error_msg}), e.response.status_code
        
    except Exception as e:
        error_msg = f'Error inesperado: {str(e)}'
        logger.error(error_msg)
        return jsonify({'error': error_msg}), 500

@app.route('/api/requerimiento/<numero>', methods=['GET'])
def get_requerimiento(numero):
    """
    Obtiene los datos de un requerimiento desde la intranet
    """
    try:
        # Validar que el número sea válido
        if not numero.isdigit():
            return jsonify({'error': 'Número de requerimiento inválido'}), 400
        
        # Construir la URL
        url = f'{REQUERIMIENTO_URL}?Requerimiento={numero}'
        logger.info(f'Accediendo a: {url}')
        
        # Crear sesión con autenticación
        session = get_auth_session()
        
        # Hacer la petición a la intranet
        response = session.get(url, timeout=30)
        response.raise_for_status()
        
        # Verificar que la respuesta tenga contenido
        if not response.text or len(response.text) < 100:
            return jsonify({'error': 'Respuesta vacía o inválida del servidor'}), 500
        
        logger.info(f'Respuesta recibida: {len(response.text)} caracteres')
        
        return jsonify({
            'success': True,
            'html': response.text,
            'url': url,
            'size': len(response.text)
        })
        
    except requests.exceptions.Timeout:
        error_msg = f'Timeout al acceder a requerimiento {numero}'
        logger.error(error_msg)
        return jsonify({'error': error_msg}), 408
        
    except requests.exceptions.ConnectionError:
        error_msg = f'No se puede conectar con la intranet. Verifica la red corporativa.'
        logger.error(error_msg)
        return jsonify({'error': error_msg}), 503
        
    except requests.exceptions.HTTPError as e:
        error_msg = f'Error HTTP {e.response.status_code}: {e.response.reason}'
        logger.error(error_msg)
        return jsonify({'error': error_msg}), e.response.status_code
        
    except Exception as e:
        error_msg = f'Error inesperado: {str(e)}'
        logger.error(error_msg)
        return jsonify({'error': error_msg}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint no encontrado'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Error interno del servidor'}), 500

if __name__ == '__main__':
    port = 5000
    
    print(f"""
🚀 Servidor Proxy iniciado en: http://localhost:{port}
📋 Endpoints disponibles:
   • GET /health - Verificar estado del servidor
   • GET /api/funcionalidad/<numero> - Obtener datos de funcionalidad
   • GET /api/requerimiento/<numero> - Obtener datos de requerimiento

🔐 Autenticación: Automática (usando credenciales de Windows)
💡 Para usar con la aplicación web, configura la URL base como: http://localhost:{port}
""")
    
    try:
        app.run(host='0.0.0.0', port=port, debug=True)
    except KeyboardInterrupt:
        print("\n👋 Servidor detenido por el usuario")
    except Exception as e:
        print(f"❌ Error al iniciar el servidor: {e}")
        sys.exit(1)
