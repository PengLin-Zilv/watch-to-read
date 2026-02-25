import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable


def generate_pdf(content: dict, output_path: str) -> str:
    """
    Main function: takes structured content dict, writes a PDF to output_path.
    Returns the output path.
    """
    doc = SimpleDocTemplate(
        output_path,
        pagesize=LETTER,
        leftMargin=1.2 * inch,
        rightMargin=1.2 * inch,
        topMargin=1.2 * inch,
        bottomMargin=1.2 * inch,
    )

    styles = _build_styles()
    story = []

    # --- Title Page ---
    story.append(Spacer(1, 1.5 * inch))
    story.append(Paragraph(content["title"], styles["Title"]))
    story.append(Spacer(1, 0.3 * inch))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CCCCCC")))
    story.append(Spacer(1, 0.3 * inch))

    # --- Summary ---
    story.append(Paragraph("Overview", styles["SectionHeader"]))
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph(content["summary"], styles["Body"]))
    story.append(Spacer(1, 0.5 * inch))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#EEEEEE")))
    story.append(Spacer(1, 0.5 * inch))

    # --- Chapters ---
    for i, chapter in enumerate(content["chapters"], start=1):
        # Chapter title
        story.append(Paragraph(chapter["chapter_title"], styles["ChapterTitle"]))
        story.append(Spacer(1, 0.2 * inch))

        # Chapter content — split by newline to preserve paragraphs
        paragraphs = chapter["content"].split("\n\n")
        for para in paragraphs:
            para = para.strip()
            if para:
                story.append(Paragraph(para, styles["Body"]))
                story.append(Spacer(1, 0.15 * inch))

        # Key concepts
        story.append(Spacer(1, 0.1 * inch))
        story.append(Paragraph("Key Concepts", styles["KeyConceptsHeader"]))
        story.append(Spacer(1, 0.05 * inch))
        concepts = "  ·  ".join(chapter["key_concepts"])
        story.append(Paragraph(concepts, styles["KeyConcepts"]))

        # Divider between chapters
        if i < len(content["chapters"]):
            story.append(Spacer(1, 0.4 * inch))
            story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#EEEEEE")))
            story.append(Spacer(1, 0.4 * inch))

    doc.build(story)
    return output_path


def _build_styles() -> dict:
    """
    Define all custom paragraph styles.
    """
    base = getSampleStyleSheet()

    styles = {
        "Title": ParagraphStyle(
            "Title",
            fontSize=28,
            fontName="Helvetica-Bold",
            textColor=colors.HexColor("#1A1A1A"),
            spaceAfter=12,
            leading=36,
        ),
        "SectionHeader": ParagraphStyle(
            "SectionHeader",
            fontSize=11,
            fontName="Helvetica-Bold",
            textColor=colors.HexColor("#888888"),
            spaceAfter=6,
            leading=16,
        ),
        "ChapterTitle": ParagraphStyle(
            "ChapterTitle",
            fontSize=18,
            fontName="Helvetica-Bold",
            textColor=colors.HexColor("#1A1A1A"),
            spaceAfter=8,
            leading=24,
        ),
        "Body": ParagraphStyle(
            "Body",
            fontSize=11,
            fontName="Helvetica",
            textColor=colors.HexColor("#333333"),
            leading=18,
            spaceAfter=6,
        ),
        "KeyConceptsHeader": ParagraphStyle(
            "KeyConceptsHeader",
            fontSize=9,
            fontName="Helvetica-Bold",
            textColor=colors.HexColor("#888888"),
            spaceAfter=4,
        ),
        "KeyConcepts": ParagraphStyle(
            "KeyConcepts",
            fontSize=10,
            fontName="Helvetica-Oblique",
            textColor=colors.HexColor("#555555"),
            leading=16,
        ),
    }

    return styles


# Local testing
if __name__ == "__main__":
    sample_content = {
        "title": "Neural Networks Explained",
        "summary": "A beginner-friendly guide to understanding how neural networks work, from basic structure to real-world applications.",
        "chapters": [
            {
                "chapter_title": "Chapter 1: What Is a Neural Network?",
                "content": "A neural network is a machine learning model inspired by the human brain.\n\nIt consists of layers of nodes, each connected to the next. Data flows through the network, getting transformed at each layer.",
                "key_concepts": ["neural network", "machine learning", "nodes"]
            },
            {
                "chapter_title": "Chapter 2: How It Learns",
                "content": "The network learns by adjusting weights during training.\n\nGradient descent helps minimize error. Backpropagation calculates how much each weight contributed to the error.",
                "key_concepts": ["weights", "gradient descent", "backpropagation"]
            }
        ]
    }

    path = generate_pdf(sample_content, "outputs/test.pdf")
    print(f"PDF generated: {path}")