from docx import Document

plantilla = "plantillaAFU2505.docx"
doc = Document(plantilla)
print("Estilos encontrados en la plantilla:")
for style in doc.styles:
    print(style.name)
