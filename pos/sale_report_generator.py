from database import Database
from PyQt5.QtWidgets import QApplication, QFileDialog
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
)
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.graphics.shapes import Drawing
import os
from collections import defaultdict


class SaleReportGenerator:
    def __init__(self, data=None, database=None):
        if database:
            self.db = database
        else: 
            self.db = Database()
        self.generate(data)

    # Generate sales report as PDF (Main Method)
    def generate(self, data):
        # Fetch sales data
        try:
            if not data:
                data = self.fetch_all_sales()
            else:
                data = data
        except Exception as e:
            raise Exception("Error fetching data from database")
        
        # File save dialog
        filename = self.sale_report_file_path()
        if not filename:
            print("PDF file save operation was canceled.")
            return

        # Create PDF document
        doc = SimpleDocTemplate(
            filename, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=72, bottomMargin=18
        )
        elements = []

        # Styles
        styles = getSampleStyleSheet()
        heading_style = styles['Heading2']
        normal_style = styles['Normal']

        # Get start and end date of sale report
        date_start = data[0]["date"].strftime("%Y-%m-%d")
        date_end = data[-1]["date"].strftime("%Y-%m-%d")

        # Cover Page and Table of Contents
        elements = self.cover_page_and_table_of_contents(elements, date_start, date_end)
        
        # 1. Executive Summary Section
        elements = self.executive_summary(elements, data)
        elements.append(Spacer(1, 12))

        # 2. Bar Chart (Sales Distribution)
        elements.append(Paragraph("2. Sales Distribution Analysis (Bar Chart)", heading_style))
        elements.append(Paragraph(
            "The bar chart below illustrates the distribution of sales over the selected period. Each bar represents the total sales amount for a specific date.",
            normal_style
        ))
        drawing = self.sale_report_bar_chart(data)
        elements.append(drawing)
        elements.append(Spacer(1, 20))

        # 3. Pie Chart (Payment Method Breakdown)
        elements.append(Paragraph("3. Payment Method Breakdown (Pie Chart)", heading_style))
        elements.append(Paragraph(
            "The pie chart below illustrates the proportion of sales made through each payment method. Each slice of the pie represents a payment method and its corresponding sales amount.",
            normal_style
        ))
        drawing = self.sale_report_pie_chart(data)
        elements.append(drawing)
        elements.append(Spacer(1, 24))

        # 4. Line Chart (Sales Trend)
        elements.append(Paragraph("4. Sales Trend Analysis (Line Chart)", heading_style))
        elements.append(Paragraph(
            "The line chart below depicts the trend of sales over time. Each point on the line represents the total sales amount for a specific date.",
            normal_style
        ))
        drawing = self.sale_report_line_chart(data)
        elements.append(drawing)
        elements.append(Spacer(1, 24))

        # 5. Monthly Sales Breakdown (Pie Chart)
        elements.append(Paragraph("5. Monthly Sales Breakdown (Pie Chart)", heading_style))
        elements.append(Paragraph(
            "The pie chart below illustrates the proportion of sales made for each month. Each slice of the pie represents a month and its corresponding sales amount.",
            normal_style
        ))
        drawing = self.sale_report_pie_chart_monthly(data)
        elements.append(drawing)
        elements.append(Spacer(1, 24))

        # 6. Histogram (Sales Amount Distribution)
        elements.append(Paragraph("6. Sales Amount Distribution (Histogram)", heading_style))
        elements.append(Paragraph(
            "The histogram below shows the distribution of sales amounts. Each bar represents the number of transactions that fall within a specific sales amount range.",
            normal_style
        ))
        drawing = self.sale_report_hist(data)
        elements.append(drawing)
        elements.append(Spacer(1, 24))

        # 7. Sales Data Table
        elements.append(Paragraph("7. Detailed Sales Data (Table)", heading_style))
        table = self.sale_report_table(data)
        elements.append(table)
        elements.append(Spacer(1, 24))

        # Build PDF
        try:
            doc.build(elements, onFirstPage=self.cover_header_footer, onLaterPages=self.add_header_footer)
            print(f"Sales report generated successfully: {filename}")
            self.db.close_connection()
        except Exception as e:
            print(f"Error generating PDF: {e}")

    # fetch sales data from database
    def fetch_all_sales(self):
        # Placeholder for fetching sales data from the database
        return self.db.fetch_all_sales()

    # get filepath for sales report
    def sale_report_file_path(self):
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getSaveFileName(
            None, "Save PDF File", "Sales_Report.pdf", "PDF files (*.pdf)", options=options
        )
        return filename

    # Daily sales data
    def daily_sales_data(self, data):
        # Get daily sales
        daily_sales = defaultdict(float)
        for sale in data:
            date = sale["date"].strftime('%Y-%m-%d')
            daily_sales[date] += float(sale["total_amount"])

        daily_sale_data = [{"date": datetime.strptime(date, '%Y-%m-%d'), "total_amount": amount} for date, amount in daily_sales.items()]

        # Sort sales data by date
        data = sorted(daily_sale_data, key=lambda x: x["date"])

        return data

    # Monthly sales data
    def monthly_sale_data(self, data):
        # Get Monthly Sale data
        monthly_sales = defaultdict(float)
        for sale in data:
            date = sale["date"].strftime('%Y-%m')
            monthly_sales[date] += float(sale["total_amount"])

        monthly_sale_data = [{"date": datetime.strptime(date, '%Y-%m'), "total_amount": amount} for date, amount in monthly_sales.items()]

        # Sort sales data by date
        monthly_sale_data = sorted(monthly_sale_data, key=lambda x: x["date"])

        return monthly_sale_data
    
    # Yearly sales data
    def yearly_sale_data(self, data):
        # Get Yearly Sale data
        yearly_sales = defaultdict(float)
        for sale in data:
            date = sale["date"].strftime('%Y')
            yearly_sales[date] += float(sale["total_amount"])

        yearly_sale_data = [{"date": datetime.strptime(date, '%Y'), "total_amount": amount} for date, amount in yearly_sales.items()]

        # Sort sales data by date
        yearly_sale_data = sorted(yearly_sale_data, key=lambda x: x["date"])

        return yearly_sale_data

    # cover page and table of contents
    def cover_page_and_table_of_contents(self, elements, date_start, date_end):
        # Styles
        styles = getSampleStyleSheet()
        title_style = styles['Title']
        heading_style = styles['Heading2']
        heading3_style = styles['Heading4']
        normal_style = styles['Normal']
        bold_style = styles['Heading1']
        # Cover Page
        elements.append(Spacer(1, 220))  
        elements.append(Image("/Users/home/Desktop/pos_system/assets/logo/logo.jpg", width=100, height=100))
        elements.append(Spacer(1, 6))  
        elements.append(Paragraph("TOKATA POS System", title_style))
        elements.append(Spacer(1, 220))
        elements.append(Paragraph(f"Annual Sales Report: {date_start} - {date_end}" , heading_style))
        elements.append(Spacer(1, 6))
        elements.append(Paragraph(f"Generated on: {datetime.now().strftime('%d %b %Y')}", heading3_style))
        elements.append(Spacer(1, 12))
        elements.append(Paragraph(
            "This comprehensive report offers a deep dive into the sales performance for the past year, analyzing key trends, "
            "payment methods, and transaction details. By examining the patterns and distributions in this report, the company "
            "can make informed decisions to optimize operations, enhance customer satisfaction, and drive growth in the future.",
            normal_style
        ))
        elements.append(PageBreak())

        # Table of Contents
        elements.append(Paragraph("Table of Contents", bold_style))
        elements.append(Spacer(1, 4))  # Reduced spacing
        elements.append(Paragraph("1. Executive Summary ", heading_style))
        elements.append(Spacer(1, 2)) # Reduced spacing
        elements.append(Paragraph("2. Sales Distribution Analysis (Bar Chart) ", heading_style))
        elements.append(Spacer(1, 4)) # Reduced spacing 
        elements.append(Paragraph("3. Payment Method Breakdown (Pie Chart) ", heading_style))
        elements.append(Spacer(1, 4)) # Reduced spacing
        elements.append(Paragraph("4. Sales Trend Analysis (Line Chart) ", heading_style))
        elements.append(Spacer(1, 4)) # Reduced spacing
        elements.append(Paragraph("5. Monthly Sales Breakdown (Pie Chart) ", heading_style))
        elements.append(Spacer(1, 4)) # Reduced spacing
        elements.append(Paragraph("6. Sales Amount Distribution (Histogram) ", heading_style))
        elements.append(Spacer(1, 4)) # Reduced spacing
        elements.append(Paragraph("7. Detailed Sales Data (Table) ", heading_style))
        elements.append(PageBreak())
        return elements

    # 1. excecutive summary section
    def executive_summary(self, elements, data):
        # Styles
        styles = getSampleStyleSheet()
        heading_style = styles['Heading2']
        normal_style = styles['Normal']

       # Executive Summary Section
        elements.append(Paragraph("1. Executive Summary", heading_style))
        elements.append(Spacer(1, 6)) # Reduced spacing
        total_sales = sum(float(sale["total_amount"]) for sale in data)
        total_transactions = len(data)
        avg_transaction = total_sales / total_transactions if total_transactions else 0

        summary = f"""
        <b>Total Sales:</b> ${total_sales:.2f}<br/><br/>
        <b>Number of Transactions:</b> {total_transactions}<br/><br/>
        <b>Average Transaction Amount:</b> ${avg_transaction:.2f}<br/><br/>
        This summary highlights key metrics that give a snapshot of overall performance, including total sales, total transactions, and the average value of each transaction.
        """
        elements.append(Paragraph(summary, normal_style)) 
        return elements
    
    # 2. sale_report bar chart
    def sale_report_bar_chart(self, data):
        data = self.daily_sales_data(data)
        # Prepare data for bar chart
        dates = [sale["date"].strftime('%Y-%m-%d') for sale in data]
        sales_amounts = [float(sale["total_amount"]) for sale in data]
        drawing = Drawing(400, 300)
        bar_chart = VerticalBarChart()
        bar_chart.x = 50
        bar_chart.y = 50
        bar_chart.width = 400
        bar_chart.height = 210
        bar_chart.data = [sales_amounts]

        # Set category names for the bar chart
        if len(dates) > 3:
            step = len(dates) // 10 or 1  # Show up to 10 labels
            bar_chart.categoryAxis.categoryNames = [dates[i] if i % step == 0 else "" for i in range(len(dates))]
        else:
            bar_chart.categoryAxis.categoryNames = dates
            
        bar_chart.categoryAxis.labels.angle = 45
        bar_chart.categoryAxis.labels.dy = -15
        bar_chart.bars[0].fillColor = colors.blue
        drawing.add(bar_chart)

        return drawing

    # 3. sale_report pie chart
    def sale_report_pie_chart(self, data):
        # Prepare data for pie chart
        payment_methods = {}
        for sale in data:
            method = sale["payment_method"]
            payment_methods[method] = payment_methods.get(method, 0) + float(sale["total_amount"])

        drawing = Drawing(500, 400)
        pie_chart = Pie()
        pie_chart.x = 100
        pie_chart.y = 100
        pie_chart.width = 225
        pie_chart.height = 225
        pie_chart.data = list(payment_methods.values())

        total_payment = sum(payment_methods.values())
        pie_chart.labels = [
            f"{method} ({amount / total_payment * 100:.1f}%)" for method, amount in payment_methods.items()
        ]

        pie_chart.slices[0].fillColor = colors.blue
        pie_chart.slices[1].fillColor = colors.green
        pie_chart.slices[2].fillColor = colors.orange

        drawing.add(pie_chart)
        return drawing

    # 4. sale_report line chart
    def sale_report_line_chart(self, data):
        data = self.monthly_sale_data(data)
        # Prepare data for line chart
        dates = [sale["date"].strftime('%Y-%m') for sale in data]
        sales_amounts = [float(sale["total_amount"]) for sale in data]

        drawing = Drawing(500, 300)
        line_chart = HorizontalLineChart()
        line_chart.x = 50
        line_chart.y = 50
        line_chart.width = 400
        line_chart.height = 200
        line_chart.data = [sales_amounts]
        line_chart.lines[0].strokeColor = colors.red

        # Set category names for the bar chart
        if len(dates) > 3:
            step = len(dates) // 10 or 1  # Show up to 10 labels
            line_chart.categoryAxis.categoryNames = [dates[i] if i % step == 0 else "" for i in range(len(dates))]
        else:
            line_chart.categoryAxis.categoryNames = dates

        # Customize the line chart
        line_chart.categoryAxis.labels.angle = 45
        line_chart.categoryAxis.labels.dy = -15
        line_chart.valueAxis.valueMin = 0
        line_chart.valueAxis.valueMax = max(sales_amounts) * 1.1
        line_chart.valueAxis.valueStep = max(sales_amounts) / 10

        drawing.add(line_chart)
        return drawing

    # 5. sale_report pie chart monthly
    def sale_report_pie_chart_monthly(self, data):
        # Prepare data for pie chart
        payment_methods = {}
        for sale in data:
            month = sale["date"].strftime('%B')
            payment_methods[month] = payment_methods.get(month, 0) + float(sale["total_amount"])

        drawing = Drawing(500, 400)
        pie_chart = Pie()
        pie_chart.x = 100
        pie_chart.y = 100
        pie_chart.width = 225
        pie_chart.height = 225
        pie_chart.data = list(payment_methods.values())

        total_payment = sum(payment_methods.values())
        pie_chart.labels = [
            f"{month} ({amount / total_payment * 100:.1f}%)" for month, amount in payment_methods.items()
        ]
        pie_chart.slices[0].fillColor = colors.blue
        pie_chart.slices[1].fillColor = colors.green
        pie_chart.slices[2].fillColor = colors.orange
        drawing.add(pie_chart)
        return drawing

    # 6. sale_report hist chart
    def sale_report_hist(self, data):
        # Prepare data for histogram
        amounts = [float(sale["total_amount"]) for sale in data]
        bins = [0, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500]
        hist_data = [0] * (len(bins) - 1)

        for amount in amounts:
            for i in range(len(bins) - 1):
                if bins[i] <= amount < bins[i + 1]:
                    hist_data[i] += 1
                    break

        drawing = Drawing(500, 300)
        bar_chart = VerticalBarChart()
        bar_chart.x = 50
        bar_chart.y = 50
        bar_chart.width = 500
        bar_chart.height = 200
        bar_chart.data = [hist_data]
        bar_chart.categoryAxis.categoryNames = [f"${bins[i]}-${bins[i + 1]}" for i in range(len(bins) - 1)]
        bar_chart.bars[0].fillColor = colors.darkblue
        drawing.add(bar_chart)
        return drawing

    # 7. sale_report data table
    def sale_report_table(self, data):
        # Prepare data for the table
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
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.lightgrey, colors.whitesmoke]),
        ]))
        return table

    # Header and Footer for cover page
    def cover_header_footer(self, canvas, doc):
        # Header
        canvas.saveState()
        canvas.setFont("Helvetica-Bold", 12)
        canvas.drawString(30, 810, "TOKATA POS System - Annual Sales Report")
        canvas.setFont("Helvetica", 10)
        canvas.drawString(30, 790, "Confidential Report")
        canvas.restoreState()

        # Footer
        canvas.saveState()
        canvas.setFont("Helvetica", 8)
        canvas.drawString(30, 20, f"Generated on: {datetime.now().strftime('%d %b %Y, %H:%M:%S')}")
        canvas.drawString(490, 20, f"@All rights reserved.")
        canvas.restoreState()

    # Header and Footer for subsequent pages
    def add_header_footer(self, canvas, doc):
        # Header
        canvas.saveState()
        canvas.setFont("Helvetica-Bold", 9)
        canvas.drawString(30, 810, "TOKATA POS System - Annual Sales Report")
        
        # Dynamic path for logo
        logo_path = os.path.join(os.path.dirname(__file__), "../assets/logo/logo.jpg")
        canvas.drawImage(logo_path, 520, 800, width=30, height=30)

        # Footer
        canvas.setFont("Helvetica", 8)
        canvas.drawString(30, 20, f"Generated on: {datetime.now().strftime('%d %b %Y, %H:%M:%S')}")
        canvas.drawString(520, 20, f"Page {doc.page - 1}")
        canvas.restoreState()
        

if __name__ == '__main__':
    report_generator = SaleReportGenerator(date_start="2015-01-01", date_end="2023-12-31")
