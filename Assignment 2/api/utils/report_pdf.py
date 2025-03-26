from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer

from io import BytesIO

data = {
    "items": [
        {
            "date": "2025-01-02",
            "description": "Restock history books",
            "code": "P-002",
            "in_qty": 10,
            "in_price": 50000,
            "in_total": 500000,
            "out_qty": 0,
            "out_price": 0,
            "out_total": 0,
            "stock_qty": [
                10,
                10
            ],
            "stock_price": [
                60000,
                50000
            ],
            "stock_total": [
                600000,
                500000
            ],
            "balance_qty": 20,
            "balance": 1100000
        },
        {
            "date": "2025-01-03",
            "description": "Sell history books to library",
            "code": "S-001",
            "in_qty": 0,
            "in_price": 0,
            "in_total": 0,
            "out_qty": 10,
            "out_price": 60000,
            "out_total": 600000,
            "stock_qty": [
                0,
                10
            ],
            "stock_price": [
                0,
                60000
            ],
            "stock_total": [
                0,
                500000
            ],
            "balance_qty": 10,
            "balance": 500000
        },
        {
            "date": "2025-01-03",
            "description": "Sell history books to library",
            "code": "S-001",
            "in_qty": 0,
            "in_price": 0,
            "in_total": 0,
            "out_qty": 5,
            "out_price": 50000,
            "out_total": 250000,
            "stock_qty": [
                0,
                5
            ],
            "stock_price": [
                0,
                50000
            ],
            "stock_total": [
                0,
                250000
            ],
            "balance_qty": 5,
            "balance": 250000
        }
    ],
    "item_code": "I-001",
    "name": "History Books",
    "unit": "Pcs",
    "summary": {
        "in_qty": 10,
        "out_qty": 15,
        "balance_qty": 5,
        "balance": 250000
    }
}

def generate(data):
    pdf_buffer = BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, 
                            pagesize=A4,
                            topMargin=50,
                            bottomMargin=50,
                            leftMargin=50,
                            rightMargin=50
                            )
    content = []

    # Add Title
    doc_title = Paragraph("<b>Stock Report</b>", ParagraphStyle(name='Title', fontSize=12, alignment=1, leading=30))
    content.append(doc_title)

    # Add Item Code, Name, and Unit
    item_code = Paragraph(f"Items Code: {data['item_code']}", ParagraphStyle(name='Item Code', fontSize=10, alignment=0, leading=12))
    item_name = Paragraph(f"Name: {data['name']}", ParagraphStyle(name='Item Name', fontSize=10, alignment=0, leading=12))
    item_unit = Paragraph(f"Unit: {data['unit']}", ParagraphStyle(name='Item Unit', fontSize=10, alignment=0, leading=12))

    content.append(item_code)
    content.append(item_name)
    content.append(item_unit)

    content.append(Spacer(1, 14))

    table_data = [
        ["No", "Date", "Description", "Code","In", "", "", "Out", "", "", "Stock", "", "",],
        ["", "", "", "", "Qty", "Price", "Total", "Qty", "Price", "Total", "Qty", "Price", "Total"],
    ]
    table_style = [
        # Text Styles
        ('FONTSIZE', (0, 0), (-1, -1), 7),  # Font size
        ('FONTNAME', (0, 0), (-1, 1), 'Helvetica-Bold'),  # Bold font
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),  # Align text to top
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # Align text to left
        ('ALIGN', (4, 0), (12, 0), 'CENTER'),  # Align text to center
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Add grid

        ('SPAN', (0, 0), (0, 1)),  # Merge No Column
        ('SPAN', (1, 0), (1, 1)),  # Merge Date Column
        ('SPAN', (2, 0), (2, 1)),  # Merge Description Column
        ('SPAN', (3, 0), (3, 1)),  # Merge Code Column
        ('SPAN', (4, 0), (6, 0)),  # Merge In Column
        ('SPAN', (7, 0), (9, 0)),  # Merge Out Column
        ('SPAN', (10, 0), (12, 0)),  # Merge Stock Column

        # Cells Padding
        ('TOPPADDING', (0, 0), (-1, -1), 5),
    ]

    # Add data to table
    index = 2
    for no, transaction in enumerate(data['items'], start=1):
        
        table_style += [
            ('SPAN', (0, index), (0, index + len(transaction['stock_qty']) - 1)),  # Merge No Column
            ('SPAN', (1, index), (1, index + len(transaction['stock_qty']) - 1)),  # Merge Date Column
            ('SPAN', (2, index), (2, index + len(transaction['stock_qty']) - 1)),  # Merge Description Column
            ('SPAN', (3, index), (3, index + len(transaction['stock_qty']) - 1)),  # Merge Code Column
            ('SPAN', (4, index), (4, index + len(transaction['stock_qty']) - 1)),  # Merge In Qty Column
            ('SPAN', (5, index), (5, index + len(transaction['stock_qty']) - 1)),  # Merge In Price Column
            ('SPAN', (6, index), (6, index + len(transaction['stock_qty']) - 1)),  # Merge In Total Column
            ('SPAN', (7, index), (7, index + len(transaction['stock_qty']) - 1)),  # Merge Out Qty Column
            ('SPAN', (8, index), (8, index + len(transaction['stock_qty']) - 1)),  # Merge Out Price Column
            ('SPAN', (9, index), (9, index + len(transaction['stock_qty']) - 1)),  # Merge Out Total Column
        ]

        for i in range(len(transaction['stock_qty'])):
            table_data.append([
                Paragraph(str(no), ParagraphStyle(name='Normal', fontSize=7, leading=10)),
                Paragraph(transaction['date'], ParagraphStyle(name='Normal', fontSize=7, leading=10)),
                Paragraph(transaction['description'], ParagraphStyle(name='Normal', fontSize=7, leading=10)),
                Paragraph(transaction['code'], ParagraphStyle(name='Normal', fontSize=7, leading=10)),
                Paragraph(str(transaction['in_qty'] if i == 0 else ""), ParagraphStyle(name='Normal', fontSize=7, leading=10)),
                Paragraph(str(transaction['in_price'] if i == 0 else ""), ParagraphStyle(name='Normal', fontSize=7, leading=10)),
                Paragraph(str(transaction['in_total'] if i == 0 else ""), ParagraphStyle(name='Normal', fontSize=7, leading=10)),
                Paragraph(str(transaction['out_qty'] if i == 0 else ""), ParagraphStyle(name='Normal', fontSize=7, leading=10)),
                Paragraph(str(transaction['out_price'] if i == 0 else ""), ParagraphStyle(name='Normal', fontSize=7, leading=10)),
                Paragraph(str(transaction['out_total'] if i == 0 else ""), ParagraphStyle(name='Normal', fontSize=7, leading=10)),
                Paragraph(str(transaction['stock_qty'][i]), ParagraphStyle(name='Normal', fontSize=7, leading=10)),
                Paragraph(str(transaction['stock_price'][i]), ParagraphStyle(name='Normal', fontSize=7, leading=10)),
                Paragraph(str(transaction['stock_total'][i]), ParagraphStyle(name='Normal', fontSize=7, leading=10))
            ])
            index += 1

        table_data.append([
            Paragraph("Balance", ParagraphStyle(name='Normal', fontSize=7, leading=10)),
            "", "", "", "", "", "", "", "", "",
            Paragraph(str(transaction['balance_qty']), ParagraphStyle(name='Normal', fontSize=7, leading=10)),
            Paragraph(str(transaction['balance']), ParagraphStyle(name='Normal', fontSize=7, leading=10)),
            ""
        ])

        table_style += [
            ('SPAN', (0, index), (3, index)),  # Merge Balance Column
            ('SPAN', (4, index), (9, index)),  # Merge Balance Column
            ('SPAN', (11, index), (12, index)),  # Merge Balance Column
        ]

        index += 1

        
    # Add summary
    table_data.append([
        Paragraph("Summary", ParagraphStyle(name='Normal', fontSize=7, leading=10)),
        "", "", "", 
        Paragraph(str(data['summary']['in_qty']), ParagraphStyle(name='Normal', fontSize=7, leading=10)),
        "", "",
        Paragraph(str(data['summary']['out_qty']), ParagraphStyle(name='Normal', fontSize=7, leading=10)),
        "", "",
        Paragraph(str(data['summary']['balance_qty']), ParagraphStyle(name='Normal', fontSize=7, leading=10)),
        Paragraph(str(data['summary']['balance']), ParagraphStyle(name='Normal', fontSize=7, leading=10)),
        "",
    ])

    table_style += [
        ('SPAN', (0, index), (3, index)),  # Merge Summary Column
        ('SPAN', (4, index), (6, index)),  # Merge Summary Column
        ('SPAN', (7, index), (9, index)),  # Merge Summary Column
        ('SPAN', (11, index), (12, index)),  # Merge Summary Column
    ]

    # Add data to table and style
    table = Table(table_data, colWidths=[20, 35, 65, 35, 30, 35, 45, 30, 35, 45, 30, 35, 45])
    style = TableStyle(table_style)

    table.setStyle(style)
    content.append(table)

    # Build the pdf
    doc.build(content)
    pdf_buffer.seek(0)
    return pdf_buffer

if __name__ == "__main__":
    pdf = generate(data)

    with open("report.pdf", "wb") as f:
        f.write(pdf.read())