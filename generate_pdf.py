import os
import re
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, KeepTogether
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# 1. Font Setup
font_path = "/System/Library/Fonts/Supplemental/Ayuthaya.ttf"
pdfmetrics.registerFont(TTFont("Ayuthaya", font_path))

# 2. Document Settings
pdf_path = "/Users/apple/Desktop/rudedog_fair_10days_content.pdf"
doc = SimpleDocTemplate(
    pdf_path,
    pagesize=A4,
    rightMargin=40,
    leftMargin=40,
    topMargin=40,
    bottomMargin=40
)

# 3. Styles
styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    'DocTitle',
    parent=styles['Heading1'],
    fontName='Ayuthaya',
    fontSize=18,
    leading=24,
    textColor=colors.HexColor('#121212'),
    alignment=1, # Center
    spaceAfter=20
)

h2_style = ParagraphStyle(
    'SectionHeader',
    parent=styles['Heading2'],
    fontName='Ayuthaya',
    fontSize=13,
    leading=18,
    textColor=colors.HexColor('#FF4D00'), # Safety Orange
    spaceBefore=14,
    spaceAfter=8,
    keepWithNext=True
)

h3_style = ParagraphStyle(
    'SubsectionHeader',
    parent=styles['Heading3'],
    fontName='Ayuthaya',
    fontSize=10,
    leading=14,
    textColor=colors.HexColor('#0E6BA8'), # Believe Blue
    spaceBefore=8,
    spaceAfter=4,
    keepWithNext=True
)

body_style = ParagraphStyle(
    'BodyText',
    parent=styles['BodyText'],
    fontName='Ayuthaya',
    fontSize=9,
    leading=14,
    textColor=colors.HexColor('#121212'),
    spaceAfter=5
)

blockquote_style = ParagraphStyle(
    'BlockCopyStyle',
    parent=styles['BodyText'],
    fontName='Ayuthaya',
    fontSize=8,
    leading=12,
    textColor=colors.HexColor('#333333'),
    leftIndent=15,
    rightIndent=15,
    spaceBefore=6,
    spaceAfter=8,
    backColor=colors.HexColor('#F5F5F3'),
    borderColor=colors.HexColor('#FF4D00'),
    borderWidth=0.5,
    borderPadding=10
)

def md_to_html(text):
    # Convert markdown bold to HTML bold tags
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    # Convert markdown italic to HTML italic tags
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
    return text

# 4. Read & Parse Markdown
md_path = "/Users/apple/.gemini/antigravity-ide/brain/8107daaa-f0f2-4535-b751-7c4d1a1f6591/rudedog_fair_10days_content.md"

if not os.path.exists(md_path):
    print(f"Error: Markdown file not found at {md_path}")
    exit(1)

with open(md_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

story = []
in_blockquote = False
blockquote_lines = []

for line in lines:
    line_str = line.strip()
    
    # Handle Blockquote accumulation
    if line_str.startswith(">"):
        in_blockquote = True
        # Strip the '>' character and any leading space
        clean_line = line_str[1:].strip()
        # Add empty line or paragraph breaks if needed
        blockquote_lines.append(md_to_html(clean_line))
        continue
    elif in_blockquote:
        # Flush blockquote
        bq_text = "<br/>".join(blockquote_lines)
        story.append(Paragraph(bq_text, blockquote_style))
        story.append(Spacer(1, 6))
        blockquote_lines = []
        in_blockquote = False

    if not line_str:
        story.append(Spacer(1, 4))
        continue
        
    if line_str.startswith("---"):
        story.append(Spacer(1, 10))
        # Draw a line separator using an empty Table with border, or simple spacer
        story.append(Spacer(1, 4))
        continue
        
    if line_str.startswith("# "):
        title_text = md_to_html(line_str[2:])
        story.append(Paragraph(title_text, title_style))
        story.append(Spacer(1, 10))
    elif line_str.startswith("## "):
        h2_text = md_to_html(line_str[3:])
        story.append(Spacer(1, 12))
        story.append(Paragraph(h2_text, h2_style))
    elif line_str.startswith("### "):
        h3_text = md_to_html(line_str[4:])
        story.append(Paragraph(h3_text, h3_style))
    elif line_str.startswith("* ") or line_str.startswith("- "):
        bullet_text = md_to_html(line_str[2:])
        story.append(Paragraph(f"• {bullet_text}", body_style))
    else:
        body_text = md_to_html(line_str)
        story.append(Paragraph(body_text, body_style))

# Final flush of blockquote in case it's at the end of the file
if in_blockquote and blockquote_lines:
    bq_text = "<br/>".join(blockquote_lines)
    story.append(Paragraph(bq_text, blockquote_style))

# 5. Build PDF document
def add_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont('Ayuthaya', 7)
    canvas.setFillColor(colors.HexColor('#85837C'))
    canvas.drawString(40, 30, "RUDEDOG FAIR 2026 — WAR ROOM CONTENT PLAN")
    canvas.drawRightString(A4[0] - 40, 30, f"Page {doc.page}")
    canvas.restoreState()

doc.build(story, onFirstPage=add_footer, onLaterPages=add_footer)
print(f"PDF successfully built and saved to: {pdf_path}")
