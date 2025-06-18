# app/utils.py

def log_to_queue(log_queue, msg):
    log_queue.put(msg)

def validar_numero_funcionalidad(num):
    return num.isdigit()
