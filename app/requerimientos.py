# app/requerimientos.py
from bs4 import BeautifulSoup
import re

def extraer_requerimiento(driver, req_url, log):
    # Ya NO abrir la pestaña aquí, solo extraer datos del requerimiento ASUMIENDO que el driver ya está en la pestaña correcta
    import time
    time.sleep(7)
    html_req = driver.page_source
    soup = BeautifulSoup(html_req, 'html.parser')
    try:
        # CORRECCIÓN: usar driver.find_element(By.TAG_NAME, "iframe") en vez de find_element_by_tag_name
        from selenium.webdriver.common.by import By
        iframe_req = driver.find_element(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframe_req)
        log("Cambiado al iframe del requerimiento.")
        time.sleep(2)
        html_req = driver.page_source
        soup = BeautifulSoup(html_req, 'html.parser')
    except Exception as e:
        log(f"No se pudo cambiar al iframe del requerimiento: {e}")
        soup = BeautifulSoup(html_req, 'html.parser')
    finally:
        driver.switch_to.default_content()
    # ...extraer campos como en logic.py...
    campos = {
        'Fecha alta': '',
        'Título': '',
        'Necesidad': '',
        'Implementación sugerida': '',
        'Cliente': '',
        'Relevamientos asociados': '',
        'Documento número': '',
        'Link': '',
        'Interacciones relacionadas': ''
    }
    documento_num = ''
    documento_link = ''
    incidente_num = ''
    incidente_link = ''
    for row in soup.find_all('tr'):
        celdas = row.find_all(['td', 'th'])
        if len(celdas) >= 2:
            label = celdas[0].get_text(strip=True)
            valor = celdas[1].get_text(strip=True)
            if 'fecha alta' in label.lower():
                campos['Fecha alta'] = valor
            elif 'nombre' in label.lower():
                campos['Título'] = valor
            elif 'necesidad' in label.lower():
                campos['Necesidad'] = valor
            elif 'implem. sugerida' in label.lower():
                campos['Implementación sugerida'] = valor
            elif 'cliente' in label.lower():
                campos['Cliente'] += valor
            elif 'requerido por' in label.lower():
                campos['Relevamientos asociados'] = valor
            elif 'documento' == label.lower():
                doc_num_match = re.search(r'(\d+)', valor)
                if doc_num_match:
                    documento_num = doc_num_match.group(1)
                    campos['Documento número'] = documento_num
                else:
                    campos['Documento número'] = ''
                link_tag = celdas[1].find('a', href=True)
                if link_tag:
                    href = link_tag['href']
                    js_match = re.search(r"window.open\('([^']+)'", href)
                    if js_match:
                        documento_link = js_match.group(1)
                    else:
                        documento_link = href
            elif 'observación' in label.lower():
                campos['Interacciones relacionadas'] = valor
    incidente_tag = soup.find('a', href=True, text=re.compile(r'\d{6,}'))
    if incidente_tag:
        incidente_num = incidente_tag.get_text(strip=True)
        href = incidente_tag['href']
        js_match = re.search(r"window.open\('([^']+)'", href)
        if js_match:
            incidente_link = js_match.group(1)
        else:
            incidente_link = href
    if campos['Cliente']:
        match = re.match(r"(\d+)(.*)", campos['Cliente'])
        if match:
            nro_cliente = match.group(1).strip()
            desc = match.group(2).strip()
            if desc:
                campos['Cliente'] = f"{nro_cliente} - {desc}"
            else:
                campos['Cliente'] = nro_cliente
    if documento_num:
        campos['Relevamientos asociados'] = ''
        campos['Documento número'] = documento_num
    else:
        campos['Relevamientos asociados'] = 'no hay'
        campos['Documento número'] = 'no hay'
        documento_link = ''
    for k in ['Fecha alta', 'Título', 'Necesidad', 'Implementación sugerida', 'Cliente']:
        if not campos[k]:
            campos[k] = 'no hay'
    return campos, documento_num, documento_link, incidente_num, incidente_link
