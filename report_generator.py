"""
PDF report generation using ReportLab.
"""
import os
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from config import Config


class ReportGenerator:
    """Generate downloadable PDF analytics reports."""

    def __init__(self, reports_dir: str | None = None):
        self.reports_dir = reports_dir or Config.REPORTS_DIR
        os.makedirs(self.reports_dir, exist_ok=True)

    def generate_customer_report(self, data: dict) -> str:
        """
        Create a PDF report with customer prediction details.
        Returns the file path of the generated report.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"customer_report_{timestamp}.pdf"
        filepath = os.path.join(self.reports_dir, filename)

        doc = SimpleDocTemplate(filepath, pagesize=letter)
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            "CustomTitle",
            parent=styles["Heading1"],
            fontSize=20,
            textColor=colors.HexColor("#2c3e50"),
            spaceAfter=20,
        )
        elements = []

        elements.append(Paragraph("AI Customer Analytics Report", title_style))
        elements.append(
            Paragraph(
                f"Generated: {datetime.now().strftime('%B %d, %Y at %H:%M')}",
                styles["Normal"],
            )
        )
        elements.append(Spacer(1, 0.3 * inch))

        # Customer details table
        table_data = [
            ["Field", "Value"],
            ["Age", str(data.get("age", "N/A"))],
            ["Income (in thousands)", str(data.get("income", "N/A"))],
            ["Spending Score", str(data.get("spending_score", "N/A"))],
            ["Customer Segment", data.get("segment", "N/A")],
            ["Purchase Probability", f"{data.get('purchase_probability', 0):.1%}"],
            ["Churn Risk", f"{data.get('churn_risk', 0):.1%}"],
            ["Customer Lifetime Value", f"{data.get('clv', 0):,.2f}"],
        ]

        table = Table(table_data, colWidths=[2.5 * inch, 3.5 * inch])
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#3498db")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, 0), 12),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#ecf0f1")),
                    ("GRID", (0, 0), (-1, -1), 1, colors.white),
                    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8f9fa")]),
                ]
            )
        )
        elements.append(table)
        elements.append(Spacer(1, 0.4 * inch))

        # Recommendations section
        elements.append(Paragraph("Product Recommendations", styles["Heading2"]))
        recommendations = data.get("recommendations", [])
        if isinstance(recommendations, str):
            rec_text = recommendations
        else:
            rec_lines = [
                f"• {r['name']} ({r['category']}) - {r['price']:.2f}"
                for r in recommendations
            ]
            rec_text = "<br/>".join(rec_lines) if rec_lines else "No recommendations available."
        elements.append(Paragraph(rec_text, styles["Normal"]))

        doc.build(elements)
        return filepath
