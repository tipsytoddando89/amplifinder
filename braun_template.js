const { Document, Packer, Paragraph, TextRun, AlignmentType, BorderStyle, ShadingType, WidthType } = require('docx');
const fs = require('fs');

const RESPONSE_BOX_COLOR = "F5F5F5";
const QUESTION_COLOR = "1F3864";

function responseLine(label) {
  return new Paragraph({
    spacing: { before: 60, after: 0 },
    children: [new TextRun({ text: label || "", color: "999999", italics: true, size: 20 })]
  });
}

function responseBox() {
  return [
    new Paragraph({
      spacing: { before: 100, after: 0 },
      border: { top: { style: BorderStyle.SINGLE, size: 4, color: "CCCCCC" }, bottom: { style: BorderStyle.SINGLE, size: 4, color: "CCCCCC" }, left: { style: BorderStyle.SINGLE, size: 4, color: "CCCCCC" }, right: { style: BorderStyle.SINGLE, size: 4, color: "CCCCCC" } },
      shading: { fill: RESPONSE_BOX_COLOR, type: ShadingType.CLEAR },
      indent: { left: 180, right: 180 },
      children: [new TextRun({ text: "Response: ", bold: true, size: 20, color: "555555" })]
    }),
    new Paragraph({
      spacing: { before: 0, after: 0 },
      border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: "CCCCCC" }, left: { style: BorderStyle.SINGLE, size: 4, color: "CCCCCC" }, right: { style: BorderStyle.SINGLE, size: 4, color: "CCCCCC" } },
      shading: { fill: RESPONSE_BOX_COLOR, type: ShadingType.CLEAR },
      indent: { left: 180, right: 180 },
      children: [new TextRun({ text: " ", size: 20 })]
    }),
    new Paragraph({
      spacing: { before: 0, after: 0 },
      border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: "CCCCCC" }, left: { style: BorderStyle.SINGLE, size: 4, color: "CCCCCC" }, right: { style: BorderStyle.SINGLE, size: 4, color: "CCCCCC" } },
      shading: { fill: RESPONSE_BOX_COLOR, type: ShadingType.CLEAR },
      indent: { left: 180, right: 180 },
      children: [new TextRun({ text: " ", size: 20 })]
    }),
    new Paragraph({
      spacing: { before: 0, after: 200 },
      border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: "CCCCCC" }, left: { style: BorderStyle.SINGLE, size: 4, color: "CCCCCC" }, right: { style: BorderStyle.SINGLE, size: 4, color: "CCCCCC" } },
      shading: { fill: RESPONSE_BOX_COLOR, type: ShadingType.CLEAR },
      indent: { left: 180, right: 180 },
      children: [new TextRun({ text: " ", size: 20 })]
    }),
  ];
}

function sectionHeader(num, title) {
  return new Paragraph({
    spacing: { before: 400, after: 120 },
    shading: { fill: "1F3864", type: ShadingType.CLEAR },
    indent: { left: 180, right: 180 },
    children: [new TextRun({ text: `  ${num}. ${title}`, bold: true, color: "FFFFFF", size: 28, font: "Arial" })]
  });
}

function subQuestion(text) {
  return new Paragraph({
    spacing: { before: 160, after: 60 },
    indent: { left: 360 },
    children: [new TextRun({ text: `\u25B6  ${text}`, bold: true, size: 22, color: "1F3864", font: "Arial" })]
  });
}

function bullet(text, pre) {
  return new Paragraph({
    spacing: { before: 60, after: 0 },
    indent: { left: 720, hanging: 200 },
    children: [
      new TextRun({ text: "\u2022  ", size: 20, color: "555555" }),
      pre ? new TextRun({ text: pre, bold: true, size: 20, color: "333333" }) : null,
      new TextRun({ text: text, size: 20, color: "333333" }),
    ].filter(Boolean)
  });
}

function note(text) {
  return new Paragraph({
    spacing: { before: 60, after: 60 },
    indent: { left: 540 },
    children: [new TextRun({ text: `\u2192 ${text}`, italics: true, size: 20, color: "888888" })]
  });
}

const doc = new Document({
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },
        margin: { top: 1080, right: 1080, bottom: 1080, left: 1080 }
      }
    },
    children: [
      // Title
      new Paragraph({
        spacing: { before: 0, after: 80 },
        children: [new TextRun({ text: "Braun Smart Home", bold: true, size: 40, font: "Arial", color: "1F3864" })]
      }),
      new Paragraph({
        spacing: { before: 0, after: 300 },
        border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: "C9A84C" } },
        children: [new TextRun({ text: "Discussion Questions & Response Template", size: 24, font: "Arial", color: "666666" })]
      }),

      // SECTION 1
      sectionHeader("1", "Distribution Model (must include B2C)"),

      subQuestion("Which retailers / integrators are envisioned?"),
      bullet("Custom Integrators: ", "See list attached"),
      bullet("Retail Customers: ", ""),
      ...responseBox(),

      subQuestion("Market sequencing: US first, then Europe?"),
      note("US & China at the same time"),
      note("Then Europe"),
      ...responseBox(),

      // SECTION 2
      sectionHeader("2", "Pricing & Value Proposition"),

      subQuestion("Current pricing (2\u20135x Aqara benchmarks) is very high. What is the clear consumer POD justifying this premium vs. other smart home players?"),
      ...responseBox(),

    ]
  }]
});

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync("Braun_SmartHome_Questions.docx", buf);
  console.log("Done: Braun_SmartHome_Questions.docx");
});
