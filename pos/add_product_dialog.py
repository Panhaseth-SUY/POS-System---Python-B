from PyQt5.QtWidgets import (
    QLineEdit, QDoubleSpinBox, QSpinBox, QComboBox, QPushButton, 
    QPlainTextEdit, QDialog, QApplication, QMessageBox
)
from PyQt5 import uic
from database import Database
import sys


class AddProductDialog(QDialog):
    def __init__(self, parent=None, Database=Database()):
        super(AddProductDialog, self).__init__(parent)

        # Initialize the database connection
        self.db = Database

        # Load the UI file
        uic.loadUi('ui/add_new_product_dialog.ui', self)

        # Set the title of the window
        self.setWindowTitle("TOKATA POS System - Add Product")

        # Initialize UI components and signals
        self._initialize_widgets()
        self._populate_categories()

        # Display the dialog
        self.show()

    def _initialize_widgets(self):
        # Define widgets
        self.name_lineEdit = self.findChild(QLineEdit, 'name_lineEdit')
        self.price_doubleSpinBox = self.findChild(QDoubleSpinBox, 'doubleSpinBox')
        self.quantity_spinBox = self.findChild(QSpinBox, 'quantity_spinBox')
        self.category_comboBox = self.findChild(QComboBox, 'category_comboBox')
        self.sku_lineEdit = self.findChild(QLineEdit, 'sku_lineEdit')
        self.barcode_lineEdit = self.findChild(QLineEdit, 'barcode_lineEdit')
        self.description_textEdit = self.findChild(QPlainTextEdit, 'description_plainTextEdit')
        self.add_product_button = self.findChild(QPushButton, 'add_product_button')
        self.cancel_button = self.findChild(QPushButton, 'cancel_button')

        # Connect signals
        self.add_product_button.clicked.connect(self._add_product)
        self.cancel_button.clicked.connect(self.close)

    def _populate_categories(self):
        """Populate the category combo box with data from the database."""
        self.category_comboBox.clear()

        try:
            categories = self.db.fetch_all_categories()
            for category in categories:
                self.category_comboBox.addItem(category['name'], category['id'])
        except Exception as e:
            self._show_error_message(f"Failed to load categories: {str(e)}")

    def _add_product(self):
        # Gather product details
        name = self.name_lineEdit.text().strip()
        price = self.price_doubleSpinBox.value()
        quantity = self.quantity_spinBox.value()
        category_id = self.category_comboBox.currentData()
        sku = self.sku_lineEdit.text().strip()
        barcode = self.barcode_lineEdit.text().strip()
        description = self.description_textEdit.toPlainText().strip()

        # Validate input
        if not name:
            self._show_error_message("Product name is required.")
            return
        if price <= 0:
            self._show_error_message("Price must be greater than zero.")
            return
        if quantity <= 0:
            self._show_error_message("Quantity must be greater than zero.")
            return
        if not category_id:
            self._show_error_message("Category is required.")
            return
        if not sku:
            self._show_error_message("SKU is required.")
            return
        if not barcode:
            self._show_error_message("Barcode is required.")
            return


        try:
            # Insert product into the database
            self.db.add_product(name, sku, barcode, description, price, quantity, category_id)
            # db.add_product("Lays", "Lays-001", "Lays-001", "Lays Chips", 0.75, 100, 1)
            # Show success message
            self._show_info_message("Product added successfully.")
            self.close()
        except Exception as e:
            self._show_error_message(f"Failed to add product: {str(e)}")
            raise Exception(f"Failed to add product: {str(e)}")

    def _show_error_message(self, message):
        """Display an error message to the user."""
        QMessageBox.critical(self, "Error", message)

    def _show_info_message(self, message):
        """Display an informational message to the user."""
        QMessageBox.information(self, "Success", message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AddProductDialog()
    sys.exit(app.exec_())
