# app/docx_helpers.py

def insert_paragraph_after(paragraph, text, style=None):
    new_paragraph = paragraph._parent.add_paragraph(text)
    paragraph._element.addnext(new_paragraph._element)
    if style:
        try:
            new_paragraph.style = style
        except KeyError:
            pass
    return new_paragraph

def is_empty_req_block(paragraphs, start_idx, labels):
    end_idx = start_idx + 1
    while end_idx < len(paragraphs):
        text = paragraphs[end_idx].text.strip().lower()
        if text.startswith('requerimiento nro.') or text.startswith('funcionalidad nro.'):
            break
        end_idx += 1
    for i in range(start_idx, end_idx):
        t = paragraphs[i].text.strip().lower()
        if t and not any(t.startswith(label) for label in labels):
            return False, end_idx
        if ':' in t:
            val = t.split(':',1)[1].strip()
            if val and val != 'no hay':
                return False, end_idx
    return True, end_idx

def add_hyperlink(paragraph, url, text, document, color='#009430'):
    """Agrega un hipervínculo a un párrafo usando la API de bajo nivel de python-docx."""
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    # Crear relación de hipervínculo
    r_id = document.part.relate_to(url, 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink', is_external=True)
    # Crear el elemento <w:hyperlink>
    hyperlink = OxmlElement('w:hyperlink')
    hyperlink.set(qn('r:id'), r_id)
    # Crear el run
    new_run = OxmlElement('w:r')
    rPr = OxmlElement('w:rPr')
    rStyle = OxmlElement('w:rStyle')
    rStyle.set(qn('w:val'), 'Hyperlink')
    rPr.append(rStyle)
    color_elem = OxmlElement('w:color')
    color_elem.set(qn('w:val'), color)
    rPr.append(color_elem)
    u = OxmlElement('w:u')
    u.set(qn('w:val'), 'single')
    rPr.append(u)
    new_run.append(rPr)
    t = OxmlElement('w:t')
    t.text = text
    new_run.append(t)
    hyperlink.append(new_run)
    paragraph._p.append(hyperlink)
    return paragraph
