from database import Database
from PyQt5.QtWidgets import QApplication, QFileDialog
import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.pagesizes import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import os

class InvoiceGenerator:
    def __init__(self, Database=Database()):
        self.db = Database

    def generate(self, invoice_id=None):
        sale_id = invoice_id or self.db.get_last_sale_id()
        sale = self.fetch_sales_data(sale_id)
        sale_items = self.fetch_sale_items_data(sale_id)
        
        filename = self.invoice_file_path(sale_id)
        if not filename:
            print("No filename selected. Invoice generation aborted.")
            return
        
        # Build elements for the invoice
        elements = self.build_elements(sale_id, sale, sale_items)
        
        # Calculate total height
        available_width = 76 * mm  # Example: 80mm minus margins
        total_height = self.calculate_dynamic_page_height(elements, available_width)
        total_height += 20 * mm  # Add some padding

        # Ensure minimum page height
        page_width = 80 * mm 
        min_height = 50 * mm
        page_height = max(total_height, min_height)

        # Set up the document
        page_size = (page_width, page_height)
        doc = SimpleDocTemplate(filename, pagesize=page_size, rightMargin=2 * mm, leftMargin=2 * mm, topMargin=3 * mm, bottomMargin=3 * mm)
 
        try:
            doc.build(elements, onFirstPage=self.add_header_footer)
            print(f"Invoice PDF successfully created: {filename}")
            return filename
        except Exception as e:
            print(f"Error generating invoice PDF: {e}")
        finally:
            # self.db.close_connection()
            pass

    # Open file dialog to select invoice file path
    def invoice_file_path(self, sale_id=None):
        # app = QApplication([])
        # options = QFileDialog.Options()
        default_dir = os.path.expanduser("~/desktop/pos_system/assets/invoice_pdf")
        # if not os.path.exists(default_dir):
        #     os.makedirs(default_dir)
        # filename, _ = QFileDialog.getSaveFileName(None, "Save PDF File", os.path.join(default_dir, f"Invoice-({sale_id}).pdf"), "PDF files (*.pdf)", options=options)
        # # # app.exit()
        if not os.path.exists(default_dir):
            os.makedirs(default_dir)
        filename = os.path.join(default_dir, f"Invoice-({sale_id}).pdf")
        return filename


    # Fetch sales data and sale items data from the database based on the given sale ID
    def fetch_sales_data(self, sale_id):
        return self.db.fetch_sale_by_id(sale_id)

    # Fetch sale items data based on the given sale ID
    def fetch_sale_items_data(self, sale_id):
        return self.db.get_sale_items_data(sale_id)

    # Calculate dynamic page height
    def calculate_dynamic_page_height(self, elements, page_width):
        total_height = 0
        for element in elements:
            _, height = element.wrap(page_width, 0)  # Calculate height for the given width
            total_height += height
        return total_height
    
    # Invoice Contents
    def build_elements(self, sale_id, sale, sale_items):
        styles = getSampleStyleSheet()
        title_style, normal_style, heading_style = styles['Title'], styles['Normal'], styles['Heading1']
        title_style.fontSize = 14
        normal_style.fontSize = heading_style.fontSize = 9

        # Invoice items
        elements = [
            Spacer(1, 25),
            Paragraph("TOKATA - Invoice", title_style),
            Paragraph(f"Invoice Number: {sale_id}", normal_style),
            Paragraph(f"Date: {sale['date']}", normal_style),
        ]

        table_style = TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'), # all cells alignment
            ('ALIGN', (1, 0), (1, -1), 'LEFT'), # column1 alignment
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'), # all cells alignment
            ('BACKGROUND', (0, 0), (-1, 0), (0.8, 0.8, 0.8)), # row1 background color

            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'), # row1 font
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'), # other rows font
            ('FONTSIZE', (0, 0), (-1, 0), 9), # row1 font size
            ('FONTSIZE', (0, 1), (-1, -1), 7), # other rows font size
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5), # all cells bottom padding
            ('GRID', (0, 0), (-1, -1), 0.5, (0, 0, 0)), # grid color
        ])

        self.add_sale_items_to_invoice(sale_items, elements, table_style)
        self.add_totals(sale, elements)
        self.add_contact_info(elements)
        return elements

    # Add sale items and total to invoice
    def add_sale_items_to_invoice(self, sale_items, elements, table_style):
        data = [["Item", "Qty", "Price", "Total"]]
        # Getting product name from sale items (product_id)
        for item in sale_items:
            item_name = self.db.fetch_product_by_id(item['product_id'])
            item_name = item_name['name']
            data.append([item_name, item['quantity'], f"${item['unit_price']:0.2f}", f"${item['unit_price'] * item['quantity']:0.2f}"])

        table = Table(data, colWidths=[35*mm, 12*mm, 12*mm, 12*mm], rowHeights=8*mm)
        table.setStyle(table_style)
        elements.append(Spacer(1, 12))
        elements.append(table)

    def add_totals(self, sale, elements):
        elements.append(Spacer(1, 12))
        tax_paragraph = Paragraph(f"Tax:      $0", style=ParagraphStyle(name='Normal', fontSize=9))
        elements.append(tax_paragraph)
        discount_paragraph = Paragraph(f"Discount: $0", style=ParagraphStyle(name='Normal', fontSize=9))
        elements.append(discount_paragraph)
        total_paragraph = Paragraph(f"Total:    ${sale['total_amount']:0.2f}", style=ParagraphStyle(name='Normal', fontSize=9))
        elements.append(total_paragraph)

    def add_contact_info(self, elements): 
        elements.append(Spacer(1, 12))
        _ = Paragraph("--------------------------------------------", style=ParagraphStyle(name='Normal', fontSize=8))
        elements.append(_)
        contact_paragraph = Paragraph(f"Contact us for any queries.", style=ParagraphStyle(name='Normal', fontSize=8))
        elements.append(contact_paragraph)
        phone = Paragraph(f"Phone: +1 123-456-7890", style=ParagraphStyle(name='Normal', fontSize=8))
        elements.append(phone)
        email = Paragraph(f"Email: panhaseth453@gmail.com", style=ParagraphStyle(name='Normal', fontSize=8))
        elements.append(email)
        address = Paragraph(f"Address: Phnom Penh, Chroy Changvar, Prek Leab, NR6.", style=ParagraphStyle(name='Normal', fontSize=8))
        elements.append(address)


    def add_header_footer(self, canvas, doc):
        width, height = doc.pagesize

        # Header
        canvas.saveState()
        canvas.setFont("Helvetica-Bold", 8)
        canvas.drawString(2 * mm, height - 7 * mm, "-TOKATA POS-")

        # Dynamic path for logo
        logo_path = os.path.join(os.path.dirname(__file__), "../assets/logo/logo.jpg")
        if os.path.exists(logo_path):
            canvas.drawImage(logo_path, width - 13 * mm, height - 9 * mm, width=5 * mm, height=5 * mm)
        else:
            canvas.setFont("Helvetica", 6)
            canvas.drawString(width - 20 * mm, height - 5 * mm, "[No Logo]")

        # Footer
        canvas.setFont("Helvetica", 8)
        canvas.drawString(2 * mm, 5 * mm, "@ All rights reserved.")
        canvas.restoreState()


if __name__ == "__main__":
    invoice_generator = InvoiceGenerator().generate()
