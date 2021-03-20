import fpdf
from datetime import date
from reader import Reader
import os

TEAL = 149, 208, 247
TAN = 237, 222, 205
SILK = 242, 236, 229
BLUE = 110, 155, 185
GREY = 133, 133, 133
BLACK = 0, 0, 0
WHITE = 255, 255, 255

def create_report(data):
    r = Reader(data)
    maxes = r.analyze()
    reviews = r.get_helpful_reviews()

    fpdf.set_global("SYSTEM_TTFONTS", os.path.join(os.path.dirname(__file__),'fonts'))
    pdf = fpdf.FPDF('P','mm','Letter') # 216 x 279 mm
    pdf.add_font("NotoSans", style="", fname="./font/NotoSans-Regular.ttf", uni=True)
    pdf.add_font("NotoSans", style="B", fname="./font/NotoSans-Bold.ttf", uni=True)
    pdf.add_font("NotoSans", style="I", fname="./font/NotoSans-Italic.ttf", uni=True)
    pdf.add_font("NotoSans", style="BI", fname="./font/NotoSans-BoldItalic.ttf", uni=True)
    pdf.add_page()
    _set_background(pdf)
    _set_title(pdf)
    _set_intro(pdf)
    _set_body(pdf)
    _set_text_stats(pdf, maxes)
    _set_wordcloud_text(pdf)
    _set_wordclouds(pdf)
    _set_reviews(pdf, reviews)
    pdf.output('Review Analysis.pdf', 'F')

def _set_background(pdf):
    # Title block
    r, g, b = BLUE
    pdf.set_fill_color(r,g,b)
    pdf.rect(x=0,
             y=0,
             w=216,
             h=39,
             style='F')
    
    # Intro block
    r, g, b = SILK
    pdf.set_fill_color(r,g,b)
    pdf.rect(x=0,
             y=39,
             w=216,
             h=20,
             style='F')

    # Pie charts background
    r, g, b = WHITE
    pdf.set_fill_color(r,g,b)
    pdf.rect(x=0,
             y=59,
             w=216,
             h=115,
             style='F')

    # Text analysis background
    r, g, b = BLUE
    pdf.set_fill_color(r,g,b)
    pdf.rect(x=0,
             y=164,
             w=216,
             h=30,
             style='F')

    # Wordcloud background
    r, g, b = WHITE
    pdf.set_fill_color(r, g, b)
    pdf.rect(x=0,
             y=194,
             w=216,
             h=86,
             style='F')
    
def _set_title(pdf):
    # Header
    pdf.set_title(' Review Analysis')
    pdf.set_font('Courier', 'B', 32)
    r, g, b = WHITE
    pdf.set_text_color(r,g,b)
    pdf.cell(txt=' Review Analysis',
             w=40,
             h=15,
             border='L',
             ln=1)

    # Date
    r, g, b = SILK
    pdf.set_text_color(r,g,b)
    pdf.set_font('Courier', 'I', 15)
    d = date.today().strftime('  %B %d, %Y')
    pdf.cell(txt=d,
             w=20,
             h=5,
             border='L')

def _set_intro(pdf):
    pdf.set_font('Courier', size=18)
    r, g, b = BLACK
    pdf.set_text_color(r,g,b)
    pdf.cell(txt='This month, your customers said...',
             w=110,
             h=45,
             align='R',
             ln=1)

def _set_body(pdf):
    pdf.image('./visuals/all_piecharts.png',
              type='png',
              x= (216/2)-90,
              w=180,
              h=90)

def _set_text_stats(pdf, maxes):
    pos_max = maxes[1]
    neg_max = maxes[0]
    good = '   Your customers loved your ' + pos_max[0] + '...'
    bad = '         ...but your ' + neg_max[0] + ' could improve.'
    
    pdf.cell(w=216,
             h=5,
             ln=1)
    pdf.set_font('Courier', size=18)
    r, g, b = SILK
    pdf.set_text_color(r,g,b)
    pdf.cell(txt=good,
             w=170,
             h=15,
             align='L',
             ln=1,
             border=0)
    pdf.cell(w=50,h=10,ln=0)
    pdf.cell(txt=bad,
             w=135,
             h=10,
             align='R',
             ln=1,
             border=0)

def _set_wordcloud_text(pdf):
    pdf.set_font('Courier', size=14)
    r, g, b = BLACK
    pdf.set_text_color(r,g,b)
    pdf.cell(w=216,
             h=15,
             ln=1)
    pdf.cell(txt='  Positive Review Wordcloud',
             w=108,
             h=10,
             align='L',
             ln=0,
             border=0)
    pdf.cell(txt='  Negative Review Wordcloud',
             w=108,
             h=10,
             align='L',
             ln=1,
             border=0)

def _set_wordclouds(pdf):
    pdf.image('./visuals/wordcloud_all_pos.png',
              type='png',
              x=pdf.get_x()-5,
              y=pdf.get_y(),
              w=100,
              h=50)
    pdf.image('./visuals/wordcloud_all_neg.png',
              type='png',
              x=pdf.get_x()+101,
              y=pdf.get_y(),
              w=100,
              h=50)

def _set_reviews(pdf, reviews):
    pdf.add_page()
    # Positive reviews
    for i in range(2):
        pdf.set_font('NotoSans', size=18)
        r, g, b = BLACK
        pdf.set_text_color(r,g,b)
        if (pdf.get_y() > 279-10):
            pdf.add_page()
        title = 'Negative Reviews'
        if i == 0: title = 'Positive Reviews'
        pdf.cell(txt=title,
                 w=200,
                 h=15,
                 align='C',
                 ln=1,
                 border='B')
        for cat in reviews[i]:
            if (pdf.get_y() > 279-10):
                pdf.add_page()
            pdf.set_font('NotoSans', size=16)
            r, g, b = BLACK
            pdf.set_text_color(r,g,b)
            c = cat[0].upper()
            pdf.cell(txt=c+cat[1:],
                w=200,
                h=15,
                align='C',
                ln=1,
                border=0)
            for review in reviews[0][cat]:
                if (pdf.get_y() > 279-55):
                    pdf.add_page()
                pdf.set_font('NotoSans', size=10)
                r, g, b = BLACK
                pdf.set_text_color(r,g,b)
                pdf.multi_cell(txt=review,
                        w=200,
                        h=5,
                        align='J',
                        border=1)