# app/selenium_helpers.py
import time

def cambiar_iframe(driver, by, value, log=None):
    try:
        iframe = driver.find_element(by, value)
        driver.switch_to.frame(iframe)
        if log:
            log(f"Cambiado al iframe: {value}")
        return True
    except Exception as e:
        if log:
            log(f"No se pudo cambiar al iframe: {e}")
        return False

def abrir_pestania(driver, url, log=None, nro_req=None):
    driver.execute_script(f"window.open('{url}', '_blank');")
    driver.switch_to.window(driver.window_handles[-1])
    if log:
        if nro_req:
            log(f"Requerimiento {nro_req} abierto en nueva pestaña.")
        else:
            log(f"Requerimiento abierto en nueva pestaña: {url}")
    time.sleep(2)
