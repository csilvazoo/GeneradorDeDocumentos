# Generador de Documentos Funcionales

Este proyecto es una aplicación de escritorio con interfaz gráfica (Tkinter) que automatiza la extracción de datos desde la intranet de la empresa Zoo Logic y genera un documento Word (.docx) con la información de una funcionalidad y sus requerimientos asociados. Insertandolo en base a una plantilla docx de "documentos funcionales".

## Índice

- [Requisitos previos](#requisitos-previos)
- [Instalación de dependencias](#instalación-de-dependencias)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Descripción de la lógica y tecnologías](#descripción-de-la-lógica-y-tecnologías)
- [Uso de la aplicación](#uso-de-la-aplicación)
- [Generación del ejecutable (.exe)](#generación-del-ejecutable-exe)

---

## Requisitos previos

- **Python 3.8 o superior**
- **Microsoft Edge** instalado en el sistema
- **msedgedriver.exe** compatible con la versión de Edge (incluido en la carpeta del proyecto)

## Instalación de dependencias

Desde la terminal, ejecutar los siguientes comandos para instalar los paquetes necesarios:

```powershell
pip install selenium
pip install beautifulsoup4
pip install python-docx
```

- **Selenium**: Automatiza la interacción con el navegador Edge para navegar la intranet y extraer datos.
- **BeautifulSoup**: Permite parsear y extraer información de los HTML obtenidos.
- **python-docx**: Permite manipular y generar archivos Word (.docx) desde Python.

NOTA: Para tener acceso a la intranet se hace desde una PC dentro de la red de Zoo o vía VPN.

## Estructura del proyecto

- `PlantillaDev.py`: Script principal con la interfaz gráfica y la lógica de extracción y generación de documentos.
- `msedgedriver.exe`: Driver de Edge necesario para Selenium (debe estar en la misma carpeta que el script).
- `plantillaAFU2505.docx`: Plantilla Word base sobre la que se insertan los datos extraídos.
- `Zoo.ico`: Ícono personalizado para el ejecutable.
- `requerimientos_v3.docx`: Archivo Word generado como resultado.

## Descripción de la lógica y tecnologías

### 1. Interfaz gráfica (Tkinter)

- Permite al usuario ingresar el número de funcionalidad, elegir si ver el navegador, seleccionar la ruta de guardado y ejecutar el proceso.
- Muestra el progreso, logs en tiempo real, mensajes de éxito/error y permite abrir el documento generado.

### 2. Automatización web (Selenium + Edge)

- Se utiliza Selenium para abrir Microsoft Edge y navegar a la intranet.
- El driver (`msedgedriver.exe`) se busca automáticamente en la carpeta del script, compatible con distribución como .exe.
- Se automatiza el ingreso del número de funcionalidad, la navegación por iframes y la extracción de requerimientos.

### 3. Extracción de datos (BeautifulSoup)

- Se parsean los HTML de las páginas de la intranet para extraer los campos requeridos de la funcionalidad y los requerimientos.

### 4. Generación de documento Word (python-docx)

- Se utiliza una plantilla base y se insertan los datos extraídos en el formato requerido.
- Se agregan hipervínculos y se formatea el documento según las necesidades del área.

### 5. Distribución como ejecutable (.exe)

- Se utilizó **PyInstaller** para generar un ejecutable standalone.
- Se incluyó el ícono personalizado y todos los recursos necesarios (driver, plantilla, etc.).
- Comando utilizado:

```powershell
pyinstaller --onefile --icon=Zoo.ico --add-data "msedgedriver.exe;." --add-data "plantillaAFU2505.docx;." PlantillaDev.py
```

- El parámetro `--add-data` asegura que los archivos necesarios se incluyan en el ejecutable.
- El ícono personalizado se especifica con `--icon`.

## Uso de la aplicación

1. Ejecutar `PlantillaDev.py` (o el .exe generado).
2. Ingresar el número de funcionalidad.
3. Elegir si se desea ver el navegador durante el proceso.
4. Seleccionar la ruta de guardado del documento Word.
5. Hacer clic en "Generar Documento".
6. Visualizar el progreso y los logs.
7. Abrir el documento generado desde la misma interfaz.

![1749044579249](image/README/1749044579249.png)

---

## Notas adicionales

- El driver de Edge debe ser compatible con la versión instalada de Microsoft Edge.
- Si se distribuye como .exe, todos los archivos necesarios deben estar en la misma carpeta o ser incluidos con PyInstaller.
- La aplicación está lista para ser utilizada en cualquier PC con Windows y Microsoft Edge instalado.
