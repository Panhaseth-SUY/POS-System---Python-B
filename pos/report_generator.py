from database import Database
from PyQt5.QtWidgets import QApplication, QFileDialog
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.shapes import Drawing
from decimal import Decimal


class ReportGenerator:
    def __init__(self):
        self.db = Database()

    def fetch_all_sales(self):
        # Placeholder for fetching sales data from the database
        return self.db.fetch_all_sales()

    def generate_sales_report_as_pdf(self):
        data = self.fetch_all_sales()
        if not data:
            print("No sales found to generate the report.")
            return

        # File save dialog
        app = QApplication([])
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getSaveFileName(None, "Save PDF File", "Sales_Report.pdf", "PDF files (*.pdf)", options=options)
        app.exit()

        if not filename:
            print("--> PDF file save operation was canceled.")
            return

        # Create PDF document
        doc = SimpleDocTemplate(filename, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=72, bottomMargin=18)
        elements = []

        # Styles
        styles = getSampleStyleSheet()
        title_style = styles['Title']
        normal_style = styles['Normal']

        # Cover page title
        elements.append(Paragraph("Sales Report", title_style))
        elements.append(Spacer(1, 24))
        elements.append(Paragraph(f"Generated on: {datetime.now().strftime('%d %b %Y, %H:%M:%S')}", normal_style))
        elements.append(Spacer(1, 48))

        # Summary section
        total_sales = sum(float(sale["total_amount"]) for sale in data)  # Convert to float
        total_transactions = len(data)
        avg_transaction = total_sales / total_transactions if total_transactions else 0

        summary = f"""
        <b>Summary:</b><br/>
        Total Sales: ${total_sales:.2f}<br/>
        Number of Transactions: {total_transactions}<br/>
        Average Transaction Amount: ${avg_transaction:.2f}
        """
        elements.append(Paragraph(summary, normal_style))
        elements.append(Spacer(1, 24))

        # Add bar chart
        drawing = Drawing(400, 200)
        chart = VerticalBarChart()
        chart.x = 50
        chart.y = 50
        chart.width = 300
        chart.height = 125
        chart.data = [[float(sale["total_amount"]) for sale in data]]  # Convert to float
        chart.categoryAxis.categoryNames = [sale["date"].strftime('%Y-%m-%d %H:%M:%S') for sale in data]
        chart.bars[0].fillColor = colors.darkblue
        chart.valueAxis.labels.fontName = "Helvetica-Bold"
        chart.categoryAxis.labels.fontName = "Helvetica-Bold"
        chart.categoryAxis.labels.angle = 45
        drawing.add(chart)
        elements.append(drawing)
        elements.append(Spacer(1, 24))

        # Table with sales data
        table_data = [["ID", "Date", "Total Amount", "Cashier", "Payment Method"]] + [
            [sale["id"], sale["date"].strftime('%Y-%m-%d %H:%M:%S'), f"${float(sale['total_amount']):.2f}", sale["cashier_id"], sale["payment_method"]]
            for sale in data
        ]

        table = Table(table_data, colWidths=[50, 100, 100, 100, 120])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))

        elements.append(table)
        elements.append(Spacer(1, 24))
        elements.append(PageBreak())

        # Build PDF
        try:
            doc.build(elements, onFirstPage=self.add_header_footer, onLaterPages=self.add_header_footer)
            print(f"--> Sales report generated successfully: {filename}")
        except Exception as e:
            print(f"Error generating PDF: {e}")

    def add_header_footer(self, canvas, doc):
        # Add header
        canvas.saveState()
        canvas.setFont("Helvetica-Bold", 9)
        canvas.drawString(30, 810, "TOKATA POS System")
        canvas.drawImage("/Users/home/Desktop/pos_system/assets/logo/logo.jpg", 520, 800, width=30, height=30)

        # Add footer
        canvas.setFont("Helvetica", 8)
        canvas.drawString(30, 20, f"Generated on: {datetime.now().strftime('%d %b %Y, %H:%M:%S')}")
        canvas.drawString(520, 20, f"Page {doc.page}")
        canvas.restoreState()


if __name__ == '__main__':
    report_generator = ReportGenerator()
    report_generator.generate_sales_report_as_pdf()
