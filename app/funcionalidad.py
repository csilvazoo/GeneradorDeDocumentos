# app/funcionalidad.py
from bs4 import BeautifulSoup

def extraer_funcionalidad(html_func, numero_funcionalidad):
    soup_func = BeautifulSoup(html_func, 'html.parser')
    campos_func = {
        'Funcionalidad nro.': numero_funcionalidad,
        'Nombre': '',
        'Descripción': '',
        'Producto': '',
        'Equipo': '',
        'Fecha alta': ''
    }
    for row_idx, row in enumerate(soup_func.find_all('tr')):
        celdas = row.find_all(['td', 'th'])
        for idx, celda in enumerate(celdas):
            texto = celda.get_text(strip=True).lower().replace(':','').replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u')
            if texto == 'nombre' and not campos_func['Nombre'] and idx+1 < len(celdas):
                campos_func['Nombre'] = celdas[idx+1].get_text(strip=True)
            elif texto == 'descripcion' and not campos_func['Descripción'] and idx+1 < len(celdas):
                campos_func['Descripción'] = celdas[idx+1].get_text(strip=True)
            elif texto in ['producto', 'productos'] and not campos_func['Producto']:
                valor = ''
                if idx+1 < len(celdas):
                    valor = celdas[idx+1].get_text(strip=True)
                    if not valor:
                        inner_table = celdas[idx+1].find('table')
                        if inner_table:
                            valor = inner_table.get_text(strip=True)
                if not valor:
                    filas = soup_func.find_all('tr')
                    if row_idx+1 < len(filas):
                        next_row = filas[row_idx+1]
                        next_celdas = next_row.find_all(['td', 'th'])
                        if idx < len(next_celdas):
                            valor = next_celdas[idx].get_text(strip=True)
                            if not valor:
                                inner_table = next_celdas[idx].find('table')
                                if inner_table:
                                    valor = inner_table.get_text(strip=True)
                campos_func['Producto'] = valor
            elif texto == 'equipo' and not campos_func['Equipo'] and idx+1 < len(celdas):
                campos_func['Equipo'] = celdas[idx+1].get_text(strip=True)
            elif texto == 'fecha alta' and not campos_func['Fecha alta']:
                valor = ''
                if idx+1 < len(celdas):
                    valor = celdas[idx+1].get_text(strip=True)
                    if not valor:
                        inner_table = celdas[idx+1].find('table')
                        if inner_table:
                            valor = inner_table.get_text(strip=True)
                if not valor:
                    filas = soup_func.find_all('tr')
                    if row_idx+1 < len(filas):
                        next_row = filas[row_idx+1]
                        next_celdas = next_row.find_all(['td', 'th'])
                        if idx < len(next_celdas):
                            valor = next_celdas[idx].get_text(strip=True)
                            if not valor:
                                inner_table = next_celdas[idx].find('table')
                                if inner_table:
                                    valor = inner_table.get_text(strip=True)
                campos_func['Fecha alta'] = valor
    for k in campos_func:
        if not campos_func[k]:
            campos_func[k] = 'no hay'
    return campos_func
