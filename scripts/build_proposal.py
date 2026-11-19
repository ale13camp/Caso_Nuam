"""Genera el documento de clase 10 a partir de la propuesta revisable en Markdown.

Requiere python-docx. Ejecutar con el runtime de documentos o instalarlo aparte.
"""

from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

ROOT = Path(__file__).resolve().parent.parent


def build():
    document = Document()
    section = document.sections[0]
    section.page_width = Inches(8.5)
    section.page_height = Inches(11)
    section.top_margin = section.bottom_margin = Inches(0.8)
    section.left_margin = section.right_margin = Inches(0.9)
    normal = document.styles['Normal']
    normal.font.name = 'Calibri'
    normal.font.size = Pt(11)
    normal.paragraph_format.space_after = Pt(8)
    normal.paragraph_format.line_spacing = 1.1
    for name in ('Title', 'Heading 1', 'Heading 2'):
        style = document.styles[name]
        style.font.name = 'Calibri'
        style.font.color.rgb = RGBColor(0, 0, 0)
    document.styles['Title'].font.size = Pt(27)
    document.styles['Heading 1'].font.size = Pt(17)
    document.styles['Heading 1'].paragraph_format.space_before = Pt(16)
    document.styles['Heading 1'].paragraph_format.space_after = Pt(9)
    # Eliminar bordes decorativos heredados de la plantilla predeterminada de Word.
    for style in document.styles:
        for border in list(style.element.iter(qn('w:pBdr'))):
            border.getparent().remove(border)
    document.styles['Subtitle'].font.color.rgb = RGBColor(80, 80, 80)
    section.header.paragraphs[0].text = 'INACAP   |   Proyecto Integrado TIHV43'
    section.header.paragraphs[0].runs[0].font.size = Pt(9)
    footer = section.footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    footer.add_run('Unidad 3 · Clase 10   |   ')
    field = OxmlElement('w:fldSimple')
    field.set(qn('w:instr'), 'PAGE')
    footer._p.append(field)
    document.add_paragraph('PROPUESTA DE PROYECTO', style='Subtitle')
    document.add_paragraph('Mantenedor de calificaciones tributarias NUAM DJ 1948', style='Title')
    document.add_paragraph(
        'Implementación de la solución\nPropuesta inicial de la clase 10', style='Subtitle'
    )
    document.add_paragraph('\nDestinatario\nnuam')
    document.add_paragraph('Equipo\nMauro Valdivia\nAlejandra Campusano\nPolette Henríquez')
    document.add_paragraph('Carrera\nIngeniería en Informática')
    document.add_paragraph('Docente\nSebastián Álvarez Trujillo')
    document.add_paragraph('Paralelo A\n18 de noviembre de 2026\nChile')
    note = document.add_paragraph(
        'Sede y número de grupo por confirmar. Documento inicial sujeto a revisión del equipo.'
    )
    note.runs[0].italic = True
    note.runs[0].font.size = Pt(10)
    document.add_page_break()
    source = (ROOT / 'docs/propuesta-clase10.md').read_text(encoding='utf-8')
    body = source[source.index('## Presentación') :]
    for block in body.split('\n\n'):
        block = block.strip()
        if not block:
            continue
        if block.startswith('## '):
            title = block[3:]
            if title == 'Objetivo general':
                document.add_page_break()
            document.add_heading(title, level=1)
        elif block.startswith('1. '):
            for line in block.splitlines():
                document.add_paragraph(line[3:], style='List Number')
        else:
            document.add_paragraph(block)
    document.core_properties.title = (
        'Propuesta inicial del mantenedor de calificaciones tributarias NUAM DJ 1948'
    )
    document.core_properties.author = 'Equipo NUAM · Valdivia Campusano Henríquez'
    document.core_properties.subject = 'Unidad 3 Clase 10'
    output = ROOT / 'docs/Propuesta_NUAM_Clase10.docx'
    document.save(output)
    print(output)


if __name__ == '__main__':
    build()
