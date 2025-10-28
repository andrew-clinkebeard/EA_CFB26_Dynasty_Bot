from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Frame, PageTemplate, FrameBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from datetime import datetime
import reportlab

def create_newspaper_pdf(title, subtitle, author, recap_text, filename="recap_newspaper.pdf"):
    # --- Setup document ---
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=36, leftMargin=36,
        topMargin=36, bottomMargin=36
    )

    # --- Styles ---
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='NewspaperTitle', fontName='Times-Bold', fontSize=24, leading=28, alignment=1))
    styles.add(ParagraphStyle(name='Subtitle', fontName='Times-Italic', fontSize=14, leading=16, alignment=1))
    styles.add(ParagraphStyle(name='Byline', fontName='Times-Roman', fontSize=10, leading=12, alignment=1, spaceAfter=12))
    styles.add(ParagraphStyle(name='Body', fontName='Times-Roman', fontSize=11, leading=14, alignment=4))

    # --- Frames for 2-column layout ---
    frame_width = (letter[0] - doc.leftMargin - doc.rightMargin - 0.25 * inch) / 2
    frame_height = letter[1] - doc.topMargin - doc.bottomMargin

    frame1 = Frame(doc.leftMargin, doc.bottomMargin, frame_width, frame_height, id='col1')
    frame2 = Frame(doc.leftMargin + frame_width + 0.25 * inch, doc.bottomMargin, frame_width, frame_height, id='col2')

    template = PageTemplate(id='TwoCol', frames=[frame1, frame2])
    doc.addPageTemplates([template])

    # --- Story content ---
    story = []
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
    print(f"✅ Newspaper-style PDF created: {filename}")


# --- Example usage ---
if __name__ == "__main__":
    recap_text = """It was a game that will be remembered for years to come. The crowd roared as both teams traded momentum swings, and the lead changed hands four times in the final quarter...

    (Continue your 500–1000 word recap here)
    """

    create_newspaper_pdf(
        title="Epic Showdown: Alabama vs Georgia Ends in Thriller",
        subtitle="Back-and-forth battle sees heroic comeback in final minutes",
        author="Harrison Dunham",
        recap_text=recap_text
    )
