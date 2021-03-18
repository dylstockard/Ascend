from fpdf import FPDF
from datetime import date

WHITE = (240, 240, 240)
PINK = (247, 86, 124)
SILK = (255, 250, 227)
GREEN = (132, 137, 74)
BLACK = (93, 87, 107)

def create_report():
    pdf = FPDF(format='letter') # 216 x 279 mm
    pdf.add_page()
    _set_background(pdf)
    _set_title(pdf)
    pdf.output('Review Analysis.pdf', 'F')

def _set_background(pdf):
    # Title block
    r, g, b = SILK
    pdf.set_fill_color(r,g,b)
    pdf.rect(x=0,
             y=0,
             w=216,
             h=39,
             style='F')
    
    # Postive customer intro block
    r, g, b = GREEN
    pdf.set_fill_color(r,g,b)
    pdf.rect(x=0,
             y=39,
             w=216,
             h=20,
             style='F')

    # Positive customer body block
    r, g, b = WHITE
    pdf.set_fill_color(r,g,b)
    pdf.rect(x=0,
             y=59,
             w=216,
             h=60,
             style='F')

    # Positive customer reviews block
    r, g, b = SILK
    pdf.set_fill_color(r,g,b)
    pdf.rect(x=0,
             y=119,
             w=216,
             h=40,
             style='F')
    
    # Negative customer intro block
    r, g, b = GREEN
    pdf.set_fill_color(r,g,b)
    pdf.rect(x=0,
             y=159,
             w=216,
             h=20,
             style='F')

    # Negative customer body block
    r, g, b = WHITE
    pdf.set_fill_color(r,g,b)
    pdf.rect(x=0,
             y=179,
             w=216,
             h=60,
             style='F')

    # Negative customer reviews block
    r, g, b = SILK
    pdf.set_fill_color(r,g,b)
    pdf.rect(x=0,
             y=239,
             w=216,
             h=40,
             style='F')


def _set_title(pdf):
    # Header
    pdf.set_font('Courier', 'B', 30)
    r, g, b = PINK
    pdf.set_text_color(r,g,b)
    pdf.cell(txt=' Review Analysis',
             w=40,
             h=15,
             border='L',
             ln=1)

    # Date
    r, g, b = BLACK
    pdf.set_text_color(r,g,b)
    pdf.set_font('Courier', 'I', 15)
    d = date.today().strftime('  %B %d, %Y')
    pdf.cell(txt=d,
             w=20,
             h=5,
             border='L')
   