from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QPushButton, QStackedWidget, QLabel, QTableWidget, QTableWidgetItem, QLineEdit,
    QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5 import uic
import sys
from database import Database
from sale_report_generator import SaleReportGenerator
from add_product_dialog import AddProductDialog
from datetime import datetime

class Admin(QMainWindow):
    def __init__(self):
        super(Admin, self).__init__()

        # Initialize the database connection
        self.db = Database()

        # Load the UI file
        uic.loadUi('ui/admin.ui', self)

        # Set window properties
        self.setWindowTitle("TOKATA POS System - Admin Window")
        self.showFullScreen()

        # Initialize UI components and Set up signals
        self._initialize_widgets()
        self._connect_signals()

        # Initialize the product widget Connect signals for product management
        self._initialize_product_widget()
        self._connect_product_signals()

        # Initialize the sale widget Connect signals for sale management
        self._initialize_sale_widget()
        self._connect_sale_signals()

        # Show the application
        self.show()



    #! UI components Management Functions =================================================================
    def _initialize_widgets(self):
        """Define and initialize widgets used in the Admin panel."""
        # Sidebar buttons
        self.dashboard_button = self.findChild(QPushButton, 'dashboard_button')
        self.categories_button = self.findChild(QPushButton, 'categories_button')
        self.products_button = self.findChild(QPushButton, 'products_button')
        self.pos_button = self.findChild(QPushButton, 'pos_button')
        self.sales_button = self.findChild(QPushButton, 'sales_button')
        self.users_button = self.findChild(QPushButton, 'users_button')
        self.setting_button = self.findChild(QPushButton, 'setting_button')
        self.signout_button = self.findChild(QPushButton, 'signout_button')

        # User information
        self.user_name = self.findChild(QLabel, 'user_name')
        self.user_picture = self.findChild(QLabel, 'user_picture')

        # Stacked widget for pages
        self.stackedWidget = self.findChild(QStackedWidget, 'stackedWidget')

    def _connect_signals(self):
        """Connect signals to their respective slots."""
        # Sidebar navigation
        self.dashboard_button.clicked.connect(lambda: self._change_page(0))
        self.categories_button.clicked.connect(lambda: self._change_page(1))
        self.products_button.clicked.connect(lambda: self._change_page(2))
        self.pos_button.clicked.connect(lambda: self._change_page(3))
        self.sales_button.clicked.connect(lambda: self._change_page(4))
        self.users_button.clicked.connect(lambda: self._change_page(5))
        self.setting_button.clicked.connect(lambda: self._change_page(6))
        self.signout_button.clicked.connect(self.signout)

    def _change_page(self, index):
        """Change the current page in the stacked widget."""
        self.stackedWidget.setCurrentIndex(index)

    def signout(self):
        """Handle user signout."""
        self.close()

    def _show_error_message(self, message):
        """Display an error message to the user."""
        QMessageBox.critical(self, "Error", message)

    def _show_info_message(self, message):
        """Display an informational message to the user."""
        QMessageBox.information(self, "Information", message)



    #! Product Management Functions =======================================================================
    def _initialize_product_widget(self):
        # Products widgets
        self.products_table = self.findChild(QTableWidget, 'products_table')
        self.add_product_button = self.findChild(QPushButton, 'add_product_pushButton')
        self.update_product_button = self.findChild(QPushButton, 'update_product_pushButton')
        self.export_excel_button = self.findChild(QPushButton, 'export_excel_pushButton')
        self.import_excel_button = self.findChild(QPushButton, 'import_excel_pushButton')
        self.delete_product_button = self.findChild(QPushButton, 'delete_pushButton')
        self.reload_button = self.findChild(QPushButton, 'reload_pushButton')
        self.search_product_lineedit = self.findChild(QLineEdit, 'search_product_lineEdit')
        self.search_product_button = self.findChild(QPushButton, 'search_product_pushButton')

    def _connect_product_signals(self):
        # Product management
        self.add_product_button.clicked.connect(self.add_product)
        self.update_product_button.clicked.connect(self.update_product)
        self.export_excel_button.clicked.connect(self.export_excel)
        self.import_excel_button.clicked.connect(self.import_excel)
        self.delete_product_button.clicked.connect(self.delete_product)
        self.reload_button.clicked.connect(self.reload_all_products)
        self.search_product_button.clicked.connect(self.search_product)
        self.search_product_lineedit.textChanged.connect(self.search_product)

        # Populate the products table
        self.reload_all_products()

    def add_product(self):
        dialog = AddProductDialog(self)
        dialog.exec_()
        self.reload_all_products()  

    def update_product(self):
        # edit the selected product
        selected_row = self.products_table.currentRow()
        if selected_row < 0:
            self._show_error_message("No selected product.")
            return

        product_id = self.products_table.item(selected_row, 0).text()
        product_name = self.products_table.item(selected_row, 1).text()
        product_stock_quantity = self.products_table.item(selected_row, 2).text()
        product_price = self.products_table.item(selected_row, 3).text()
        category = self.products_table.item(selected_row, 4).text()
        product_sku = self.products_table.item(selected_row, 5).text()
        product_barcode = self.products_table.item(selected_row, 6).text()
        product_description = self.products_table.item(selected_row, 7).text()

        category_id = self.db.fetch_category_by_name(category)
        category_id = category_id['id']

        try:
            self.db.update_product(product_id=product_id, name=product_name, stock_quantity=product_stock_quantity, price=product_price, category_id=category_id, sku=product_sku, barcode=product_barcode, description=product_description)
            self.reload_all_products() 
            self._show_info_message(f"Product ({product_id}) has been updated successfully")
        except Exception as e:
            print(f"Error editing product: {e}")
            self._show_error_message("Failed to edit product.")

    def import_excel(self):
        try:
            self.db.add_products_from_dataset()
            self.reload_all_products()
            self._show_info_message("Products imported from Excel successfully.")
        except Exception as e:
            print(f"Error importing products from Excel: {e}")
            self._show_error_message("Failed to import products from Excel.")
 
    def export_excel(self):
        try:
            self.db.save_products_table_as_excel_file()
            self._show_info_message("Products exported to Excel successfully.")
        except Exception as e:
            print(f"Error exporting products to Excel: {e}")
            self._show_error_message("Failed to export products to Excel.")

    def delete_product(self):
        # delete the selected product
        selected_row = self.products_table.currentRow()
        if selected_row < 0:
            self._show_error_message("No selected product.")
            return

        product_id = self.products_table.item(selected_row, 0).text()
        product_name = self.products_table.item(selected_row, 1).text()
        try:
            if self.db.is_product_referenced(product_id):
                self.db.soft_delete_product(product_id)
            else:
                self.db.delete_product(product_id)
            self.reload_all_products()
            self._show_info_message(f"Product ({product_name}-{product_id}) has been deleted successfully.")
        except Exception as e:
            print(f"Error deleting product: {e}")
            self._show_error_message("Failed to delete product.")

    def reload_products_table(self):
        # clear all products from table
        self.products_table.clear()
        self.products_table.setRowCount(0)

        try:
            # Fetch all products from the database
            self.products = self.db.fetch_all_products()

            # Define column headers
            headers = ["ID", "Name", "Stock Quantity", "Price ($)", "Category", 
                       "SKU", "Barcode", "Description", "Created At", "Updated At"]

            # Set the row and column count dynamically
            self.products_table.setRowCount(len(self.products)+28)
            self.products_table.setColumnCount(len(headers))
            self.products_table.setHorizontalHeaderLabels(headers)

            # Set the selection behavior to highlight entire rows
            self.products_table.setSelectionBehavior(QTableWidget.SelectRows)
            self.products_table.setSortingEnabled(True)

            #Dynamically resize the table
            self.products_table.horizontalHeader().setSectionResizeMode(1)

            # Populate the table with data
            for row_index, product in enumerate(self.products):
                self.products_table.setItem(row_index, 0, QTableWidgetItem(str(product['id'])))
                self.products_table.setItem(row_index, 1, QTableWidgetItem(product['name']))
                self.products_table.setItem(row_index, 2, QTableWidgetItem(str(product['stock_quantity'])))
                self.products_table.setItem(row_index, 3, QTableWidgetItem(f"{product['price']:.2f}"))
                category = self.db.fetch_category_by_id(product['category_id'])
                self.products_table.setItem(row_index, 4, QTableWidgetItem(category['name']))
                self.products_table.setItem(row_index, 5, QTableWidgetItem(product['sku']))
                self.products_table.setItem(row_index, 6, QTableWidgetItem(product['barcode']))
                self.products_table.setItem(row_index, 7, QTableWidgetItem(product['description']))
                self.products_table.setItem(row_index, 8, QTableWidgetItem(product['created_at'].strftime('%Y-%m-%d')))
                self.products_table.setItem(row_index, 9, QTableWidgetItem(product['updated_at'].strftime('%Y-%m-%d')))

            # Columns to make non-editable (e.g., ID)
            non_editable_columns = {0,8,9}

            # Populate the table with data
            for row_index, product in enumerate(self.products):
                for col_index, value in enumerate([
                    str(product['id']),
                    product['name'],
                    str(product['stock_quantity']),
                    f"{product['price']:.2f}",
                    self.db.fetch_category_by_id(product['category_id'])['name'],
                    product['sku'],
                    product['barcode'],
                    product['description'],
                    product['created_at'].strftime('%Y-%m-%d'),
                    product['updated_at'].strftime('%Y-%m-%d'),
                ]):
                    item = QTableWidgetItem(value)

                    # Disable editing for specified columns
                    if col_index in non_editable_columns:
                        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

                    self.products_table.setItem(row_index, col_index, item)

            self.products_table.setSortingEnabled(True)
        except Exception as e:
            print(f"Error loading products: {e}")
            self._show_error_message("Failed to load products.")

    def reload_all_products(self):
        self.products = self.db.fetch_all_products()
        self.reload_products_table()

    def search_product(self):
        search_term = self.search_product_lineedit.text().strip().lower()
        try:
            if search_term:
                self.products = self.db.search_products_by_name(search_term)
            else:
                self.products = self.db.fetch_all_products()
            self.reload_products_table()
        except Exception as e:
            print(f"Error searching products: {e}")
            self._show_error_message("Failed to search products.")



    #! Sale Management Functions ==========================================================================
    def _initialize_sale_widget(self):
        # Initialize the sale widget here
        self.date_start = self.findChild(QLabel, 'date_start_dateEdit')
        self.date_end = self.findChild(QLabel, 'date_end_dateEdit')
        self.update_sale_button = self.findChild(QPushButton, 'update_sale_pushButton')
        self.sale_import_excel_button = self.findChild(QPushButton, 'sale_import_excel_pushButton')
        self.sale_pdf_report_button = self.findChild(QPushButton, 'pdf_report_pushButton')
        self.delete_sale_button = self.findChild(QPushButton, 'delete_sale_pushButton')
        self.reload_sale_button = self.findChild(QPushButton, 'reload_pushButton_2')
        self.search_sale_lineedit = self.findChild(QLineEdit, 'search_sale_lineEdit')
        self.search_sale_button = self.findChild(QPushButton, 'search_sale_pushButton')
        self.sales_table = self.findChild(QTableWidget, 'sales_table')

    def _connect_sale_signals(self):
        # Connect signals for sale management
        self.update_sale_button.clicked.connect(self.update_sale)
        self.sale_import_excel_button.clicked.connect(self.import_sale)
        self.sale_pdf_report_button.clicked.connect(self.generate_pdf_report)
        self.delete_sale_button.clicked.connect(self.delete_sale)
        self.reload_sale_button.clicked.connect(self.reload_all_sales)
        self.search_sale_button.clicked.connect(self.reload_sales_table)
        self.search_sale_lineedit.textChanged.connect(self.reload_sales_table)

        # Populate the sales table
        self.reload_all_sales()

    def update_sale(self):
        selected_row = self.sales_table.currentRow()
        if selected_row < 0:
            self._show_error_message("No selected sale.")
            return

        sale_id = self.sales_table.item(selected_row, 0).text()
        total_amount = self.sales_table.item(selected_row, 2).text()
        cashier_id = self.sales_table.item(selected_row, 3).text()
        cashier_name = self.sales_table.item(selected_row, 4).text()
        payment_method = self.sales_table.item(selected_row, 5).text()

        if not total_amount or not cashier_id or not cashier_name or not payment_method:
            self._show_error_message("Please fill in all required fields.")
            return

        try:
            self.db.update_sale(sale_id=sale_id, cashier_id=cashier_id, cashier_name=cashier_name, total_amount=total_amount, payment_method=payment_method)
            self.reload_all_sales()
            self._show_info_message(f"Sale ({sale_id}) has been updated successfully.")
        except Exception as e:
            self._show_error_message(f"Error updating sale: {str(e)}")

    def import_sale(self):
        try:
            self.db.add_sales_from_dataset()
            self.reload_all_sales()
            self._show_info_message("Sales imported from Excel successfully.")
        except Exception as e:
            self._show_error_message(f"Error importing sales from Excel: {str(e)}")

    def generate_pdf_report(self):
        try: 
            SaleReportGenerator(date_start="2015-01-01", date_end="2023-12-31")
            self._show_info_message("PDF report generated successfully.")
        except Exception as e:
            self._show_error_message(f"Error generating PDF report: {str(e)}")

    def delete_sale(self):
        selected_row = self.sales_table.currentRow()
        if selected_row < 0:
            self._show_error_message("No selected sale.")
            return

        sale_id = self.sales_table.item(selected_row, 0).text()

        try:
            self.db.delete_sale(sale_id)
            self.reload_all_sales()
            self._show_info_message(f"Sale ({sale_id}) has been deleted successfully.")
        except Exception as e:
            self._show_error_message(f"Error deleting sale: {str(e)}")

    def reload_sales_table(self):
        self.sales_table.clear()
        self.sales_table.setColumnCount(8)
        self.sales_table.setHorizontalHeaderLabels(["ID", "Date", "Total Amount ($)", "Cashier ID", 
                                                    "Cashier Name", "Payment Method", "Status", "Date Edited"])
        
        sales_data = self.sales
        self.sales_table.setRowCount(len(sales_data)+28)
        self.sales_table.setSortingEnabled(False)

        # Populate table with sales data
        for row_index, sale in enumerate(sales_data):
            self.sales_table.setItem(row_index, 0, QTableWidgetItem(str(sale['id'])))
            self.sales_table.setItem(row_index, 1, QTableWidgetItem(sale['date'].strftime('%Y-%m-%d')))
            self.sales_table.setItem(row_index, 2, QTableWidgetItem(f"{sale['total_amount']:.2f}"))
            self.sales_table.setItem(row_index, 3, QTableWidgetItem(str(sale['cashier_id'])))
            self.sales_table.setItem(row_index, 4, QTableWidgetItem(sale['cashier_name']))
            self.sales_table.setItem(row_index, 5, QTableWidgetItem(sale['payment_method']))
            self.sales_table.setItem(row_index, 6, QTableWidgetItem(sale['status']))
            self.sales_table.setItem(row_index, 7, QTableWidgetItem(sale['updated_at'].strftime('%Y-%m-%d')))


        # Columns to make non-editable (e.g., ID)
        non_editable_columns = {0, 1, 7}

        # Populate the table with data
        for row_index, sale in enumerate(self.sales):
            for col_index, value in enumerate([
            str(sale['id']),
            sale['date'].strftime('%Y-%m-%d'),
            f"{sale['total_amount']:.2f}",
            str(sale['cashier_id']),
            sale['cashier_name'],
            sale['payment_method'],
            sale['status'],
            sale['updated_at'].strftime('%Y-%m-%d'),
            ]):
               item = QTableWidgetItem(value)

            # Disable editing for specified columns
            if col_index in non_editable_columns:
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

            self.sales_table.setItem(row_index, col_index, item)

        # set column width to fit with table width
        self.sales_table.horizontalHeader().setSectionResizeMode(1)
        self.sales_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.sales_table.setSortingEnabled(True)

    def reload_all_sales(self):
        self.sales = self.db.fetch_all_sales()
        self.reload_sales_table() 




# TODO: Run Admin Page
if __name__ == "__main__":
    app = QApplication(sys.argv)
    admin_window = Admin()
    sys.exit(app.exec_())
