from database import Database
from PyQt5 import uic
from PyQt5.QtWidgets import QLineEdit, QPushButton, QComboBox, QMessageBox
from PyQt5.QtWidgets import QDialog, QApplication


class AddUserDialog(QDialog):
    def __init__(self, parent=None, db=None):
        super(AddUserDialog, self).__init__(parent)

        # Initialize the database connection
        self.db = db if db else Database()

        # Load the UI file
        uic.loadUi('ui/add_new_user_dialog.ui', self)

        # Set the title of the window
        self.setWindowTitle("Add User Dialog")

        # Initialize UI components and signals
        self._initialize_widgets()

        # Display the dialog
        self.show()

    def _initialize_widgets(self):
        # Define widgets
        self.name_lineEdit = self.findChild(QLineEdit, 'name_lineEdit')
        self.username_lineEdit = self.findChild(QLineEdit, 'username_lineEdit')
        self.password_lineEdit = self.findChild(QLineEdit, 'password_lineEdit')
        self.confirm_password_lineEdit = self.findChild(QLineEdit, 'confirm_password_lineEdit')
        self.role_comboBox = self.findChild(QComboBox, 'role_comboBox')
        self.add_user_button = self.findChild(QPushButton, 'add_pushButton')
        self.cancel_button = self.findChild(QPushButton, 'cancel_pushButton')

        # Connect signals
        self.add_user_button.clicked.connect(self._add_user)
        self.cancel_button.clicked.connect(self.reject)

        self.name_lineEdit.returnPressed.connect(self.username_lineEdit.setFocus)
        self.username_lineEdit.returnPressed.connect(self.password_lineEdit.setFocus)
        self.password_lineEdit.returnPressed.connect(self.confirm_password_lineEdit.setFocus)
        self.confirm_password_lineEdit.returnPressed.connect(self.role_comboBox.setFocus)

    def _add_user(self):
        # Gather user details
        name = self.name_lineEdit.text().strip()
        username = self.username_lineEdit.text().strip()
        password = self.password_lineEdit.text().strip()
        confirm_password = self.confirm_password_lineEdit.text().strip()
        role = self.role_comboBox.currentText()

        # Validate user details
        if not name or not username or not password or not confirm_password:
            self._show_error_message("Please fill in all fields.")
            return

        if password != confirm_password:
            self._show_error_message("Passwords do not match.")
            return

        # Add the user to the database
        try:
            self.db.add_user(name=name, username=username, password=password, role=role)
            self._show_info_message("User added successfully.")
            self.accept()
        except Exception as e:
            self._show_error_message(f"Failed to add user: {str(e)}")

    def _show_error_message(self, message):
        """Display an error message to the user."""
        QMessageBox.critical(self, "Error", message)

    def _show_info_message(self, message):
        """Display an informational message to the user."""
        QMessageBox.information(self, "Information", message)


if __name__ == '__main__':
    app = QApplication([])
    dialog = AddUserDialog()
    dialog.exec_()
