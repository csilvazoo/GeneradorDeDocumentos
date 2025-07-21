# Changelog

Todas las versiones siguen el formato CalVer-incremental: YY.MM.DD.N (desde 25.06.25.1).

## [25.06.25.1+]

### Cambios

- Nuevo formato de versionado: YY.MM.DD.N generado automáticamente por el pipeline.
- El archivo VERSION, el nombre del .exe y la GUI muestran la versión en este formato.
- Sincronización automática de VERSION entre pipeline y repositorio.

## [25.06.25.1]

### Agregado

- Barra de progreso oculta hasta ejecución.
- Actualización automática de .docx desde la GUI.
- Pipeline de Azure DevOps para generación automática del .exe.

### Corregido

- Error visual de barra verde inicial.
- Eliminación de etiquetas duplicadas en la GUI.

## [25.06.10.1]

### Agregado

- Refactorización completa: lógica, GUI y recursos separados.
- Integración de Selenium y generación de documentos Word.
- Mejoras de logs y usabilidad.
