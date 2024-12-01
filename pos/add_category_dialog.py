from database import Database
from PyQt5 import uic
from PyQt5.QtWidgets import QLineEdit, QPushButton, QMessageBox, QDialog, QApplication, QPlainTextEdit


class AddCategoryDialog(QDialog):
    """Dialog for adding a new category."""

    def __init__(self, parent=None, database=None):
        """Initialize the dialog."""
        super().__init__(parent)

        # Initialize the database connection
        self.db = database if database else Database()

        # Load the UI file
        uic.loadUi('ui/add_new_category_dialog.ui', self)

        # Set the title of the window
        self.setWindowTitle("Add Category Dialog")

        # Initialize UI components and signals
        self._initialize_widgets()

        # Display the dialog
        self.show()

    def _initialize_widgets(self):
        """Initialize the UI components and connect signals."""
        self.category_name_line_edit = self.findChild(QLineEdit, 'name_lineEdit')
        self.category_description_plain_text_edit = self.findChild(QPlainTextEdit, 'plainTextEdit')
        self.add_category_button = self.findChild(QPushButton, 'add_pushButton')
        self.cancel_button = self.findChild(QPushButton, 'cancel_pushButton')

        # Connect signals
        self.add_category_button.clicked.connect(self._add_category)
        self.cancel_button.clicked.connect(self.close)
        self.category_name_line_edit.returnPressed.connect(self.category_description_plain_text_edit.setFocus)

    def _add_category(self):
        """Add a new category to the database."""
        # Gather category details
        name = self.category_name_line_edit.text().strip()
        description = self.category_description_plain_text_edit.toPlainText().strip()

        # Validate category details
        if not name:
            self._show_error_message("Please enter a category name.")
            return

        # Add category to the database
        try:
            self.db.add_category(name, description)
            self._show_success_message("Category added successfully.")
            self.close()
        except Exception as e:
            self._show_error_message(f"Failed to add category. Error: {str(e)}")

    def _show_error_message(self, message):
        """Show an error message."""
        QMessageBox.critical(self, "Error", message)

    def _show_success_message(self, message):
        """Show a success message."""
        QMessageBox.information(self, "Success", message)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    dialog = AddCategoryDialog()
    sys.exit(app.exec_())
