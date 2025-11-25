from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Image, ListFlowable, ListItem, FrameBreak
)
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
import os

def create_three_frame_layout(
        output_file="three_frame_layout.pdf",
        image_path="example.jpg",
        bullet_items=None,
        body_text=""
):
    if bullet_items is None:
        bullet_items = ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5"]

    styles = getSampleStyleSheet()
    title_style = styles['Title']
    body_style = styles['BodyText']

    # --- Document Setup ---
    doc = BaseDocTemplate(output_file, pagesize=letter,
                          leftMargin=36, rightMargin=36,
                          topMargin=36, bottomMargin=36)

    page_width, page_height = letter

    # --- Frame Sizes ---
    title_height = 0.7 * inch
    top_section_height = 3.5 * inch
    bottom_section_height = page_height - title_height - top_section_height - doc.topMargin - doc.bottomMargin

    frame_padding = 12

    # --- Define Frames ---

    # Title frame (full width)
    frame_title = Frame(
        doc.leftMargin,
        page_height - title_height - doc.topMargin,
        page_width - doc.leftMargin - doc.rightMargin,
        title_height,
        id='title_frame',
        showBoundary=1
    )

    image_frame_width = (page_width - doc.leftMargin - doc.rightMargin) / 2 - frame_padding
    image_fram_height = 451.5 #page_height - title_height - top_section_height - doc.topMargin
    print(image_frame_width)
    # Frame 1: Image (top-left)
    frame_left = Frame(
        doc.leftMargin,
        image_fram_height,
        image_frame_width,
        top_section_height,
        id='frame_left',
        showBoundary=1
    )

    # Frame 2: Bulleted list (top-right)
    frame_right = Frame(
        doc.leftMargin + (page_width - doc.leftMargin - doc.rightMargin) / 2 + frame_padding,
        page_height - title_height - top_section_height - doc.topMargin,
        (page_width - doc.leftMargin - doc.rightMargin) / 2 - frame_padding,
        top_section_height,
        id='frame_right',
        showBoundary=1
    )

    # Frame 3: Body text, full width across the bottom
    frame_bottom = Frame(
        doc.leftMargin,
        doc.bottomMargin,
        page_width - doc.leftMargin - doc.rightMargin,
        bottom_section_height,
        id='frame_bottom',
        showBoundary=1
    )

    # --- Create Page Template ---
    template = PageTemplate(
        id='three_frame_template',
        frames=[frame_title, frame_left, frame_right, frame_bottom]
    )

    doc.addPageTemplates([template])

    # --- Flowables for each section ---
    story = []

    # Title
    story.append(Paragraph("Your Document Title", title_style))

    # Image
    #image default size is 1024x1792 - need to keep that ratio
    img = Image(image_path, width=258, height=451.5)
    story.append(img)
    story.append(FrameBreak())

    # Bulleted list
    bullets = ListFlowable(
        [ListItem(Paragraph(item, body_style)) for item in bullet_items],
        bulletType='bullet',
        start='•'
    )
    story.append(bullets)
    story.append(FrameBreak())

    # Body text (can be multiple Paragraphs)
    story.append(Paragraph(body_text, body_style))
    story.append(Paragraph(body_text, body_style))  # example second paragraph

    # --- Build document ---
    doc.build(story)

    print(f"PDF created: {output_file}")

path = (os.getcwd() + "\\test.pdf")
# Example usage:
create_three_frame_layout(
    output_file=path,
    image_path="C:\\Users\\Andrew Clinkenbeard\\source\\repos\\EA_CFB26_Dynasty_Bot\\test.png",
    bullet_items=["One", "Two", "Three", "Four", "Five"],
    body_text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. " * 10
)
