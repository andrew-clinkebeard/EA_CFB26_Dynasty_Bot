from reportlab.platypus import (
    BaseDocTemplate, Paragraph, Spacer, Frame, PageTemplate, FrameBreak, Image
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from datetime import datetime
from reportlab.lib.colors import HexColor
import os
import temp

def create_recruit_spotlight(title, subtitle, author, recap_text, output_folder=".", background_color=HexColor("#EFEECE"), image_path="./Graphics/logo_dynasty_tribune.png"):
    
    #width , height in 1/72 of an inch increments
    pageSize = (612,936) #custom page size to deal make report one page long
    
    # --- Callback: draw background on each page ---
    def draw_background(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(background_color)
        canvas.rect(0, 0, pageSize[0], pageSize[1], fill=1, stroke=0)
        canvas.restoreState()
    
    # --- Setup document ---
    doc = BaseDocTemplate(
        output_folder,
        pagesize=pageSize,
        rightMargin=36, leftMargin=36,
        topMargin=36, bottomMargin=36
    )

    # --- Styles ---
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='NewspaperTitle', fontName='Times-Bold', fontSize=24, leading=28, alignment=1))
    styles.add(ParagraphStyle(name='Subtitle', fontName='Times-Italic', fontSize=14, leading=16, alignment=1))
    styles.add(ParagraphStyle(name='Byline', fontName='Times-Roman', fontSize=10, leading=12, alignment=1, spaceAfter=12))
    styles.add(ParagraphStyle(name='Body', fontName='Times-Roman', fontSize=11, leading=14, alignment=4))

    # --- 3 frames top right and left and bottom 2/3 rds ---
    top_frame_width = (pageSize[0] - doc.leftMargin - doc.rightMargin - 0.25 * inch) / 2
    bottome_frame_width = pageSize[0] - doc.leftMargin - doc.rightMargin
    top_frame_height = (pageSize[1] - (doc.topMargin + doc.bottomMargin)) * (1/3)
    bottom_frame_height = (pageSize[1] - doc.topMargin - doc.bottomMargin) - top_frame_height
    
    #top left cordinates
    top_left_x1 = doc.leftMargin
    top_left_y1 = doc.height - top_frame_height
    
    #top right cordinates 
    top_right_x1 = doc.leftMargin + top_frame_width + 0.25 * inch
    top_right_y1 = doc.height - doc.topMargin - top_frame_height
    
    #bottom cordinates
    bottom_x1 = doc.leftMargin
    bottom_y1 = doc.bottomMargin

    #top left
    frame1 = Frame(top_left_x1, top_left_y1, top_frame_width, top_frame_height, id='topleft', showBoundary=1)
    #top right
    frame2 = Frame(top_right_x1, top_right_y1, top_frame_width, top_frame_height, id='topright', showBoundary=1)
    #bottom
    frame3 = Frame(bottom_x1, bottom_y1, bottome_frame_width, bottom_frame_height, id='bottom', showBoundary=1)

    template = PageTemplate(id='recruitPage', frames=[frame1, frame2, frame3], onPage=draw_background)
    doc.addPageTemplates([template])

    # --- Story content ---
    story = []
    # Add logo at the top if provided
    scale = .5
    if image_path and os.path.exists(image_path):
        logo = Image(image_path, width=3*scale*inch, height=2*scale*inch)  # adjust size as needed
        logo.hAlign = 'CENTER'
        story.append(logo)
        story.append(Spacer(1, 12))


    story.append(Paragraph(title, styles['NewspaperTitle']))
    if subtitle:
        story.append(Paragraph(subtitle, styles['Subtitle']))
    story.append(Paragraph(f"By {author} | {datetime.now().strftime('%B %d, %Y')}", styles['Byline']))
    story.append(Spacer(1, 12))

    # Split recap into paragraphs
    paragraphs = recap_text.split('\n')
    for p in paragraphs:
        if p.strip():
            story.append(Paragraph(p.strip(), styles['Body']))
            story.append(Spacer(1, 6))

    # --- Build the PDF ---
    doc.build(story)
    print(f"Newspaper-style PDF created: {output_folder}")
    return output_folder


output_folder =os.getcwd() + "\\test.pdf"
create_recruit_spotlight(
        title="Epic Showdown: Alabama vs Georgia Ends in Thriller",
        subtitle="Back-and-forth battle sees heroic comeback in final minutes",
        author="Harrison Dunham",
        recap_text=temp.recapText,
        output_folder=output_folder, 
        background_color=HexColor("#FFFFFF"),
        image_path="C:\\Users\\Andrew Clinkenbeard\\source\\repos\\EA_CFB26_Dynasty_Bot\\test.png"
    )