from fpdf import FPDF
from datetime import date
from reader import Reader

WHITE = (250, 250, 250)
PINK = (247, 86, 124)
SILK = (255, 250, 227)
GREEN = (132, 137, 74)
BLACK = (93, 87, 107)

def create_report(data):
    r = Reader(data)

    pdf = FPDF(format='letter') # 216 x 279 mm
    pdf.add_page()
    _set_background(pdf)
    _set_title(pdf)
    _set_intro(pdf, True)
    _set_body(pdf, r, True)
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
    r, g, b = WHITE
    pdf.set_fill_color(r,g,b)
    pdf.rect(x=0,
             y=39,
             w=216,
             h=20,
             style='F')

    # Positive customer body block
    #r, g, b = WHITE
    #pdf.set_fill_color(r,g,b)
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
    r, g, b = WHITE
    pdf.set_fill_color(r,g,b)
    pdf.rect(x=0,
             y=159,
             w=216,
             h=20,
             style='F')

    # Negative customer body block
    #r, g, b = WHITE
    #pdf.set_fill_color(r,g,b)
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
    pdf.set_title(' Review Analysis')
    pdf.set_font('Courier', 'B', 32)
    r, g, b = PINK
    pdf.set_text_color(r,g,b)
    pdf.cell(txt=' Review Analysis',
             w=40,
             h=15,
             border='L',
             ln=2)

    # Date
    r, g, b = BLACK
    pdf.set_text_color(r,g,b)
    pdf.set_font('Courier', 'I', 15)
    d = date.today().strftime('  %B %d, %Y')
    pdf.cell(txt=d,
             w=20,
             h=5,
             border='L')

def _set_intro(pdf, pos):
    pdf.set_font('Courier', size=18)
    r, g, b = GREEN
    pdf.set_text_color(r,g,b)
    if pos:
        # positive
        pdf.cell(txt='This week, your customers loved...',
                w=110,
                h=43,
                align='R',
                ln=2)
    else:
        # Negative
        pdf.cell(txt='Your customers thought you could improve...',
                w=160,
                h=183,
                align='R')

def _set_body(pdf, data, pos):
    pdf.set_font('Courier', size=20)
    r, g, b = GREEN
    pdf.set_text_color(r,g,b)
    if pos:
        # positive

