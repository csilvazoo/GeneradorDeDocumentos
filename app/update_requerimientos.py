import os
from docx import Document
from app.docx_helpers import insert_paragraph_after, is_empty_req_block, add_hyperlink
from app.requerimientos import extraer_requerimiento
from app.funcionalidad import extraer_funcionalidad
from app.selenium_helpers import cambiar_iframe, abrir_pestania
from app.utils import log_to_queue, validar_numero_funcionalidad
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def update_requerimientos(numero_funcionalidad, docx_path, driver, log_queue):
    log = lambda msg: log_to_queue(log_queue, msg)
    # Abrir el documento seleccionado por el usuario
    document = Document(docx_path)
    # Obtener los requerimientos ya presentes en el documento
    req_nros_en_doc = set()
    for p in document.paragraphs:
        t = p.text.strip().lower()
        if t.startswith('requerimiento nro.'):
            nro = t.replace('requerimiento nro.', '').strip()
            if nro.isdigit():
                req_nros_en_doc.add(nro)
    # Navegar y obtener los requerimientos actuales de la intranet
    url = "http://reportes03/reports/report/IyD/Gestion/Funcionalidad"
    driver.get(url)
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    log("Página cargada correctamente.")
    time.sleep(3)
    cambiar_iframe(driver, By.TAG_NAME, "iframe")
    log("Cambiado al iframe del reporte.")
    input_funcionalidad = WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.ID, "ReportViewerControl_ctl04_ctl03_txtValue"))
    )
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", input_funcionalidad)
    driver.execute_script("arguments[0].focus();", input_funcionalidad)
    input_funcionalidad.click()
    input_funcionalidad.clear()
    for char in numero_funcionalidad:
        input_funcionalidad.send_keys(char)
        time.sleep(0.1)
    log(f"Número de funcionalidad {numero_funcionalidad} asignado.")
    time.sleep(0.5)
    ver_informe_btn = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "ReportViewerControl_ctl04_ctl00"))
    )
    ver_informe_btn.click()
    log("Botón 'Ver informe' clickeado dentro del iframe.")
    time.sleep(15)
    divs = driver.find_elements(By.XPATH, "//div[contains(@style, 'width:20.22mm;min-width: 20.22mm;') or contains(@style, 'width:23.24mm;min-width: 23.24mm;')]")
    requerimiento_nros = []
    requerimiento_links = []
    after_req_cliente = False
    for div in divs:
        text = div.text.strip()
        if text == "Req. Cliente":
            after_req_cliente = True
            continue
        if after_req_cliente:
            if text.isdigit() and len(text) < 7:
                nro = text
                href = f"http://reportes03/reports/report/IyD/Gestion/Requerimiento?TipoRequerimiento=1&Numero={nro}"
                requerimiento_nros.append(nro)
                requerimiento_links.append(href)
            elif text.isdigit() and len(text) >= 7:
                continue
            elif text == "Req. Cliente":
                continue
    log(f"Requerimientos encontrados: {requerimiento_nros}")
    log(f"Requerimientos existentes en el documento:")
    for idx, nro in enumerate(sorted(req_nros_en_doc), 1):
        log(f"  {idx}. {nro}")
    nuevos_reqs = [nro for nro in requerimiento_nros if nro not in req_nros_en_doc]
    log(f"Requerimientos a agregar:")
    for idx, nro in enumerate(nuevos_reqs, 1):
        log(f"  {idx}. {nro}")
    if not nuevos_reqs:
        log("No hay nuevos requerimientos para agregar al documento.")
        log("Proceso finalizado.")
        return False
    # 1. Detectar el bloque de 'Funcionalidad nro.' y sus detalles
    func_idx = None
    for i, p in enumerate(document.paragraphs):
        if p.text.strip().lower().startswith('funcionalidad nro.'):
            func_idx = i
            break
    if func_idx is not None:
        # Encontrar el final del bloque de funcionalidad
        end_func_idx = func_idx + 1
        while end_func_idx < len(document.paragraphs):
            t = document.paragraphs[end_func_idx].text.strip().lower()
            if t.startswith('requerimiento nro.'):
                break
            end_func_idx += 1
        # Extraer el bloque de funcionalidad
        func_block = document.paragraphs[func_idx:end_func_idx]
        # Eliminar el bloque de funcionalidad del documento
        for j in range(end_func_idx-1, func_idx-1, -1):
            document.paragraphs[j]._element.getparent().remove(document.paragraphs[j]._element)
        # Insertar los nuevos requerimientos donde estaba el bloque de funcionalidad
        insert_after_paragraph = document.paragraphs[func_idx-1] if func_idx > 0 else None
    else:
        func_block = []
        insert_after_paragraph = document.paragraphs[-1]
    # 2. Insertar los nuevos requerimientos
    last_p = insert_after_paragraph
    for nro in nuevos_reqs:
        idx = requerimiento_nros.index(nro)
        req_url = requerimiento_links[idx]
        abrir_pestania(driver, req_url, log, nro_req=nro)
        campos, documento_num, documento_link, incidente_num, incidente_link = extraer_requerimiento(driver, req_url, log)
        p = insert_paragraph_after(last_p, f"Requerimiento nro.{nro}", style="toa heading")
        p = insert_paragraph_after(p, f"Fecha alta: {campos['Fecha alta']}", style="List Bullet")
        p = insert_paragraph_after(p, f"Título: {campos['Título']}", style="List Bullet")
        p = insert_paragraph_after(p, f"Necesidad: {campos['Necesidad']}", style="List Bullet")
        p = insert_paragraph_after(p, f"Implementación sugerida: {campos['Implementación sugerida']}", style="List Bullet")
        p = insert_paragraph_after(p, f"Cliente: {campos['Cliente']}", style="List Bullet")
        p = insert_paragraph_after(p, f"Relevamientos asociados: {campos['Relevamientos asociados']}", style="List Bullet")
        p = insert_paragraph_after(p, f"Documento número: {campos['Documento número']}", style="List Bullet 2")
        if documento_link and documento_num:
            p = insert_paragraph_after(p, f"Link: ", style="List Bullet 2")
            add_hyperlink(p, documento_link, documento_num, document)
        else:
            p = insert_paragraph_after(p, f"Link: no hay", style="List Bullet 2")
        if incidente_num and incidente_link:
            p = insert_paragraph_after(p, f"Interacciones relacionadas: ", style="List Bullet")
            p = insert_paragraph_after(p, f"Incidente: ", style="List Bullet 2")
            add_hyperlink(p, incidente_link, incidente_num, document)
        else:
            p = insert_paragraph_after(p, f"Interacciones relacionadas: no hay", style="List Bullet")
        last_p = p
    # 3. Volver a insertar el bloque de funcionalidad después del último requerimiento
    if func_block:
        for para in func_block:
            new_p = insert_paragraph_after(last_p, para.text, style=para.style.name if hasattr(para.style, 'name') else None)
            last_p = new_p
    document.save(docx_path)
    log(f"Documento actualizado con nuevos requerimientos: {nuevos_reqs}")
    log("Proceso finalizado.")
    return True