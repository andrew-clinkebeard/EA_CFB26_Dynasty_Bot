from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    BaseDocTemplate, Paragraph, Spacer, Frame, PageTemplate, FrameBreak, Image
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from datetime import datetime
from reportlab.lib.colors import HexColor
import os

def create_newspaper_pdf(title, subtitle, author, recap_text, logo_path=None,output_folder=".", background_color=colors.whitesmoke):
    
    # --- Callback: draw background on each page ---
    def draw_background(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(background_color)
        canvas.rect(0, 0, letter[0], letter[1], fill=1, stroke=0)
        canvas.restoreState()

    # --- Setup document ---
    # --- Timestamp ---
    now = datetime.now()
    timestamp_str = now.strftime("%Y%m%d%H%M%S")

    # --- Build folder + filename ---
    final_filename = os.path.join(output_folder, f"Harrydbear_{timestamp_str}.pdf")

    doc = BaseDocTemplate(
        final_filename,
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

    template = PageTemplate(id='TwoCol', frames=[frame1, frame2], onPage=draw_background)
    doc.addPageTemplates([template])

    # --- Story content ---
    story = []
    # Add logo at the top if provided
    scale = .5
    if logo_path and os.path.exists(logo_path):
        logo = Image(logo_path, width=3*scale*inch, height=2*scale*inch)  # adjust size as needed
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
    print(f"✅ Newspaper-style PDF created: {final_filename}")


# --- Example usage ---
if __name__ == "__main__":
    recap_text = """Saturday night in Tuscaloosa delivered a clash worthy of the national spotlight. Alabama and Georgia entered Bryant-Denny Stadium with playoff implications on the line, and neither team disappointed. From the opening kickoff, the game had the rhythm of a heavyweight fight—each side landing blows, adjusting, and refusing to yield. In the end, Alabama escaped with a 31–28 victory that left fans breathless and pundits already debating where it ranks among the greatest matchups in recent SEC history.

The first quarter belonged to Georgia. Their defense came out suffocating, forcing an early turnover that set up a short field for quarterback Carson Beck. Two plays later, he found tight end Brock Bowers in the corner of the end zone for the game’s first score. Alabama’s offense struggled to find rhythm early, but the momentum shifted midway through the second quarter when Jalen Milroe connected on a deep post route to Jermaine Burton for a 65-yard touchdown. The play seemed to ignite the Crimson Tide offense and the crowd alike.

From there, the game transformed into a track meet. Georgia responded immediately with a 12-play drive capped by a Kendall Milton rushing touchdown. Alabama countered with precision passing and tempo, tying the game again before halftime on a short touchdown run by Milroe. As the teams entered the locker rooms tied 14–14, it was clear neither side was ready to back down.

The third quarter saw both defenses make key adjustments. Georgia brought more pressure off the edge, while Alabama tightened its coverage against the run. Still, explosive plays defined the evening. Early in the quarter, Georgia’s Ladd McConkey broke free for a 47-yard catch and run, putting the Bulldogs ahead 21–14. Alabama answered with a methodical 10-play drive ending in a Milroe-to-Burton connection once again. Every possession carried weight, every third down felt decisive, and every fan was on their feet.

The fourth quarter will be talked about for years. Georgia reclaimed the lead with eight minutes left on a one-yard quarterback sneak. Alabama’s next possession stalled near midfield, and the Bulldogs seemed poised to seal the win. But momentum turned abruptly when Alabama linebacker Dallas Turner strip-sacked Beck, giving the Tide the ball deep in Georgia territory. Three plays later, Milroe punched it in himself, tying the game with under four minutes to go.

Georgia’s final drive reached the Alabama 40-yard line, but a costly holding penalty pushed them back. On fourth and long, Beck’s pass was tipped at the line and intercepted by Kool-Aid McKinstry. The Tide crowd erupted. With less than a minute left, Milroe guided the offense into field goal range, and kicker Will Reichard drilled a 42-yarder as time expired.

The fourth quarter will be talked about for years. Georgia reclaimed the lead with eight minutes left on a one-yard quarterback sneak. Alabama’s next possession stalled near midfield, and the Bulldogs seemed poised to seal the win. But momentum turned abruptly when Alabama linebacker Dallas Turner strip-sacked Beck, giving the Tide the ball deep in Georgia territory. Three plays later, Milroe punched it in himself, tying the game with under four minutes to go.

Georgia’s final drive reached the Alabama 40-yard line, but a costly holding penalty pushed them back. On fourth and long, Beck’s pass was tipped at the line and intercepted by Kool-Aid McKinstry. The Tide crowd erupted. With less than a minute left, Milroe guided the offense into field goal range, and kicker Will Reichard drilled a 42-yarder as time expired.
The fourth quarter will be talked about for years. Georgia reclaimed the lead with eight minutes left on a one-yard quarterback sneak. Alabama’s next possession stalled near midfield, and the Bulldogs seemed poised to seal the win. But momentum turned abruptly when Alabama linebacker Dallas Turner strip-sacked Beck, giving the Tide the ball deep in Georgia territory. Three plays later, Milroe punched it in himself, tying the game with under four minutes to go.

Georgia’s final drive reached the Alabama 40-yard line, but a costly holding penalty pushed them back. On fourth and long, Beck’s pass was tipped at the line and intercepted by Kool-Aid McKinstry. The Tide crowd erupted. With less than a minute left, Milroe guided the offense into field goal range, and kicker Will Reichard drilled a 42-yarder as time expired.
When the dust settled, Alabama’s sideline erupted in celebration, while Georgia’s players could only watch in stunned silence. It was a game defined by resilience, by players who refused to be denied, and by momentum swings that tested every ounce of composure. For Alabama, it was another chapter in a storied legacy. For Georgia, it was heartbreak—but perhaps the kind that fuels another championship run.
"""
    
    logo_path = "logo_dynasty_tribune.png"  # <--- path to your saved logo image
output_folder = "Reports"
os.makedirs(output_folder, exist_ok=True)

create_newspaper_pdf(
    title="Epic Showdown: Alabama vs Georgia Ends in Thriller",
    subtitle="Back-and-forth battle sees heroic comeback in final minutes",
    author="Harrison Dunham",
    recap_text=recap_text,
    logo_path=logo_path,
    output_folder=output_folder,   # <--- pass folder only
    background_color=HexColor("#EFEECE")    # 🎨 Change this to any color (e.g. colors.lightgrey, colors.ivory)
)
