from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QPushButton, QStackedWidget, QLabel, QTableWidget, QTableWidgetItem, QLineEdit,
    QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5 import uic
import sys
from database import Database
from add_product_dialog import AddProductDialog

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

        # Initialize UI components
        self._initialize_widgets()

        # Set up signals
        self._connect_signals()

        # Populate the products table
        self.reload_products()

        # Show the application
        self.show()

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

        # Products widgets
        self.products_table = self.findChild(QTableWidget, 'products_table')
        self.add_product_button = self.findChild(QPushButton, 'add_product_pushButton')
        self.edit_product_button = self.findChild(QPushButton, 'update_product_pushButton')
        self.export_excel_button = self.findChild(QPushButton, 'export_excel_pushButton')
        self.import_excel_button = self.findChild(QPushButton, 'import_excel_pushButton')
        self.delete_product_button = self.findChild(QPushButton, 'delete_pushButton')
        self.reload_button = self.findChild(QPushButton, 'reload_pushButton')
        self.search_product_lineedit = self.findChild(QLineEdit, 'search_product_lineEdit')
        self.search_product_button = self.findChild(QPushButton, 'search_product_pushButton')

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

        # Product management
        self.add_product_button.clicked.connect(self.add_product)
        self.edit_product_button.clicked.connect(self.edit_product)
        self.export_excel_button.clicked.connect(self.export_excel)
        self.import_excel_button.clicked.connect(self.import_excel)
        self.delete_product_button.clicked.connect(self.delete_product)
        self.reload_button.clicked.connect(self.reload_products)
        self.search_product_button.clicked.connect(self.search_product)
        self.search_product_lineedit.textChanged.connect(self.search_product)

    def _change_page(self, index):
        """Change the current page in the stacked widget."""
        self.stackedWidget.setCurrentIndex(index)

    # Product Management Functions
    def add_product(self):
        dialog = AddProductDialog(self)
        dialog.exec_()
        self.reload_products()  # Refresh the product list after adding a new product

    def edit_product(self):
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
            self.reload_products()  # Refresh the product list after editing a product
            self._show_info_message(f"Product ({product_id}) has been updated successfully")
        except Exception as e:
            print(f"Error editing product: {e}")
            self._show_error_message("Failed to edit product.")
        
    def export_excel(self):
        try:
            self.db.save_products_table_as_excel_file()
            self._show_info_message("Products exported to Excel successfully.")
        except Exception as e:
            print(f"Error exporting products to Excel: {e}")
            self._show_error_message("Failed to export products to Excel.")

    def import_excel(self):
        try:
            self.db.add_products_from_dataset()
            self.reload_products()
            self._show_info_message("Products imported from Excel successfully.")
        except Exception as e:
            print(f"Error importing products from Excel: {e}")
            self._show_error_message("Failed to import products from Excel.")

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
            self.reload_products()
            self._show_info_message(f"Product ({product_name}-{product_id}) has been deleted successfully.")
        except Exception as e:
            print(f"Error deleting product: {e}")
            self._show_error_message("Failed to delete product.")
        
    def search_product(self):
        search_term = self.search_product_lineedit.text().strip().lower()
        try:
            if search_term:
                # Filter products directly from the database
                self.products = self.db.search_products_by_name(search_term)
            else:
                # If no search term, reload all products
                self.products = self.db.fetch_all_products()
            self.reload()
        except Exception as e:
            print(f"Error searching products: {e}")
            self._show_error_message("Failed to search products.")

    def reload(self):
        # clear all products from table
        self.products_table.clearContents()
        self.products_table.setRowCount(0)
        try:
            # Set the row and column count dynamically
            self.products_table.setRowCount(len(self.products)+28)

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

    def reload_products(self):
        # clear all products from table
        self.products_table.clearContents()
        self.products_table.setRowCount(0)
        try:
            # Fetch all products from the database
            self.products = self.db.fetch_all_products()

            # Define column headers
            headers = ["ID", "Name", "Stock Quantity", "Price", "Category", 
                       "SKU", "Barcode", "Description", "Created At", "Updated At"]

            # Set the row and column count dynamically
            self.products_table.setRowCount(len(self.products)+28)
            self.products_table.setColumnCount(len(headers))
            self.products_table.setHorizontalHeaderLabels(headers)

            # Set the selection behavior to highlight entire rows
            self.products_table.setSelectionBehavior(QTableWidget.SelectRows)

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
    
    def _show_error_message(self, message):
        """Display an error message to the user."""
        QMessageBox.critical(self, "Error", message)

    def _show_info_message(self, message):
        """Display an informational message to the user."""
        QMessageBox.information(self, "Information", message)

    def signout(self):
        """Handle user signout."""
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    admin_window = Admin()
    sys.exit(app.exec_())
