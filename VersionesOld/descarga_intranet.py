import time
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# Configuración de Edge
options = Options()
options.add_argument("--start-maximized")
# Si necesitas que no se abra la ventana, descomenta la siguiente línea:
# options.add_argument("--headless")

# Ruta al driver de Edge (msedgedriver debe estar en el PATH o especificar la ruta)
driver = webdriver.Edge(options=options)

try:
    # URL fija de la intranet
    url = "http://reportes03/reports/report/IyD/Gestion/Funcionalidad"
    driver.get(url)

    # Esperar a que cargue la página principal
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
    print("Página cargada correctamente.")

    # Espera adicional tras cargar la página para asegurar que todo el formulario esté listo
    time.sleep(3)

    # Cambiar el contexto al primer iframe (ajusta el índice si hay más de uno)
    iframe = driver.find_element(By.TAG_NAME, "iframe")
    driver.switch_to.frame(iframe)
    print("Cambiado al iframe del reporte.")

    # Buscar el campo de número de funcionalidad dentro del iframe y asignar el valor
    numero_funcionalidad = "11194"  # Puedes cambiar este valor o parametrizarlo
    input_funcionalidad = WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.ID, "ReportViewerControl_ctl04_ctl03_txtValue"))
    )
    time.sleep(1)
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", input_funcionalidad)
    time.sleep(0.5)
    driver.execute_script("arguments[0].focus();", input_funcionalidad)
    input_funcionalidad.click()
    time.sleep(0.5)
    input_funcionalidad.clear()
    time.sleep(0.5)
    for char in numero_funcionalidad:
        input_funcionalidad.send_keys(char)
        time.sleep(0.1)
    time.sleep(0.5)
    print(f"Número de funcionalidad {numero_funcionalidad} asignado.")

    # Ahora hacer click en el botón "Ver informe"
    ver_informe_btn = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "ReportViewerControl_ctl04_ctl00"))
    )
    ver_informe_btn.click()
    print("Botón 'Ver informe' clickeado dentro del iframe.")
    # Esperar a que se genere el informe (ajusta la condición según el contenido esperado)
    time.sleep(15)

    # Extraer el HTML del iframe y guardarlo en un archivo
    with open(r"c:\Users\csilva\Desktop\reporte_funcionalidad.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    print("HTML del informe guardado en reporte_funcionalidad.html")

    # Extraer los números de requerimientos asociados del HTML generado
    requerimiento_nros = set()
    import re
    with open(r"c:\Users\csilva\Desktop\reporte_funcionalidad.html", encoding="utf-8") as f:
        html = f.read()
    matches = re.findall(r"Req\. Cliente\s*(\d+)", html, re.IGNORECASE)
    requerimiento_nros.update(matches)
    matches = re.findall(r"Requerimiento nro\.?\s*(\d+)", html, re.IGNORECASE)
    requerimiento_nros.update(matches)
    print(f"Requerimientos asociados encontrados: {requerimiento_nros}")

    # Abrir cada requerimiento en una nueva pestaña
    for nro in requerimiento_nros:
        req_url = f"http://reportes03/reports/report/IyD/Gestion/Requerimiento?TipoRequerimiento=1&Numero={nro}"
        driver.execute_script(f"window.open('{req_url}', '_blank');")
        print(f"Requerimiento {nro} abierto en nueva pestaña.")

    # Esperar para que puedas ver las pestañas abiertas
    time.sleep(10)

    print("Proceso finalizado. Cierra el navegador.")
finally:
    driver.quit()
