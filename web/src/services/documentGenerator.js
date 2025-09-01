import { Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType, ExternalHyperlink } from 'docx';

/**
 * Genera un documento Word con los datos de funcionalidad y requerimientos
 * Equivalente a la generación en logic.py usando python-docx
 */
export const generateWordDocument = async (numeroFuncionalidad, funcionalidadData, requerimientosDetallados) => {
  try {
    // Crear documento base
    const doc = new Document({
      sections: [{
        properties: {},
        children: [
          // Título principal
          new Paragraph({
            children: [
              new TextRun({
                text: "ANÁLISIS FUNCIONAL DE USUARIO",
                bold: true,
                size: 32,
              }),
            ],
            heading: HeadingLevel.TITLE,
            alignment: AlignmentType.CENTER,
            spacing: { after: 400 }
          }),
          
          // Subtítulo
          new Paragraph({
            children: [
              new TextRun({
                text: `Funcionalidad ${numeroFuncionalidad}`,
                bold: true,
                size: 24,
              }),
            ],
            heading: HeadingLevel.HEADING_1,
            spacing: { before: 200, after: 300 }
          }),
          
          // Sección de Requerimientos
          new Paragraph({
            children: [
              new TextRun({
                text: "Requerimientos",
                bold: true,
                size: 20,
              }),
            ],
            heading: HeadingLevel.HEADING_2,
            spacing: { before: 400, after: 200 }
          }),
          
          // Agregar cada requerimiento
          ...await generateRequerimientosContent(requerimientosDetallados),
          
          // Datos de funcionalidad al final
          ...generateFuncionalidadContent(funcionalidadData.info || funcionalidadData),
        ],
      }],
    });
    
    // Convertir a buffer
    const buffer = await Packer.toBuffer(doc);
    return buffer;
    
  } catch (error) {
    console.error('Error al generar documento Word:', error);
    throw new Error(`Error al generar documento: ${error.message}`);
  }
};

/**
 * Genera el contenido de los requerimientos
 */
const generateRequerimientosContent = async (requerimientosDetallados) => {
  const content = [];
  
  for (const req of requerimientosDetallados) {
    // Título del requerimiento
    content.push(
      new Paragraph({
        children: [
          new TextRun({
            text: `Requerimiento nro.${req.numero}`,
            bold: true,
            size: 18,
          }),
        ],
        heading: HeadingLevel.HEADING_3,
        spacing: { before: 300, after: 100 }
      })
    );
    
    // Detalles del requerimiento con bullets
    const details = [
      { label: "Fecha alta", value: req.fechaAlta },
      { label: "Título", value: req.titulo },
      { label: "Necesidad", value: req.necesidad },
      { label: "Implementación sugerida", value: req.implementacion },
      { label: "Cliente", value: req.cliente },
      { label: "Relevamientos asociados", value: req.relevamientos },
    ];
    
    details.forEach(detail => {
      content.push(
        new Paragraph({
          children: [
            new TextRun({
              text: `${detail.label}: ${detail.value}`,
              size: 20,
            }),
          ],
          bullet: { level: 0 },
          spacing: { after: 100 }
        })
      );
    });
    
    // Documento número (con sub-bullet)
    content.push(
      new Paragraph({
        children: [
          new TextRun({
            text: `Documento número: ${req.documento}`,
            size: 20,
          }),
        ],
        bullet: { level: 1 },
        spacing: { after: 100 }
      })
    );
    
    // Link del documento
    if (req.documentoLink && req.documento && req.documento !== 'no hay') {
      content.push(
        new Paragraph({
          children: [
            new TextRun({
              text: "Link: ",
              size: 20,
            }),
            new ExternalHyperlink({
              children: [
                new TextRun({
                  text: req.documento,
                  style: "Hyperlink",
                  size: 20,
                }),
              ],
              link: req.documentoLink,
            }),
          ],
          bullet: { level: 1 },
          spacing: { after: 100 }
        })
      );
    } else {
      content.push(
        new Paragraph({
          children: [
            new TextRun({
              text: "Link: no hay",
              size: 20,
            }),
          ],
          bullet: { level: 1 },
          spacing: { after: 100 }
        })
      );
    }
    
    // Interacciones relacionadas
    if (req.incidente && req.incidenteLink) {
      content.push(
        new Paragraph({
          children: [
            new TextRun({
              text: "Interacciones relacionadas:",
              size: 20,
            }),
          ],
          bullet: { level: 0 },
          spacing: { after: 50 }
        })
      );
      
      content.push(
        new Paragraph({
          children: [
            new TextRun({
              text: "Incidente: ",
              size: 20,
            }),
            new ExternalHyperlink({
              children: [
                new TextRun({
                  text: req.incidente,
                  style: "Hyperlink",
                  size: 20,
                }),
              ],
              link: req.incidenteLink,
            }),
          ],
          bullet: { level: 1 },
          spacing: { after: 200 }
        })
      );
    } else {
      content.push(
        new Paragraph({
          children: [
            new TextRun({
              text: "Interacciones relacionadas: no hay",
              size: 20,
            }),
          ],
          bullet: { level: 0 },
          spacing: { after: 200 }
        })
      );
    }
  }
  
  return content;
};

/**
 * Genera el contenido de funcionalidad
 */
const generateFuncionalidadContent = (funcionalidadData) => {
  return [
    // Título de funcionalidad
    new Paragraph({
      children: [
        new TextRun({
          text: `Funcionalidad nro.${funcionalidadData['Funcionalidad nro.']}`,
          bold: true,
          size: 20,
        }),
      ],
      heading: HeadingLevel.HEADING_2,
      spacing: { before: 400, after: 200 }
    }),
    
    // Detalles de funcionalidad
    new Paragraph({
      children: [
        new TextRun({
          text: `Nombre: ${funcionalidadData.Nombre}`,
          size: 20,
        }),
      ],
      bullet: { level: 0 },
      spacing: { after: 100 }
    }),
    
    new Paragraph({
      children: [
        new TextRun({
          text: `Descripción: ${funcionalidadData.Descripción}`,
          size: 20,
        }),
      ],
      bullet: { level: 0 },
      spacing: { after: 100 }
    }),
    
    new Paragraph({
      children: [
        new TextRun({
          text: `Producto: ${funcionalidadData.Producto}`,
          size: 20,
        }),
      ],
      bullet: { level: 0 },
      spacing: { after: 100 }
    }),
    
    new Paragraph({
      children: [
        new TextRun({
          text: `Equipo: ${funcionalidadData.Equipo}`,
          size: 20,
        }),
      ],
      bullet: { level: 0 },
      spacing: { after: 100 }
    }),
    
    new Paragraph({
      children: [
        new TextRun({
          text: `Fecha alta: ${funcionalidadData['Fecha alta']}`,
          size: 20,
        }),
      ],
      bullet: { level: 0 },
      spacing: { after: 200 }
    }),
  ];
};
