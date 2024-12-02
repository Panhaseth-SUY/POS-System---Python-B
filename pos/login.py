
from PyQt5.QtWidgets import QMainWindow, QApplication, QLineEdit, QMessageBox, QPushButton, QCommandLinkButton, QCheckBox
from PyQt5 import uic
import sys
from database import Database


class Login(QMainWindow):
    def __init__(self):
        super(Login, self).__init__()
        # Initialize database
        self.db = Database()

        # Load the ui file 
        uic.loadUi('ui/login.ui', self)

        # Set the title of the window
        self.setWindowTitle("Login Window")
        self.showFullScreen()

        # Initailize widgets
        self.username_lineEdit = self.findChild(QLineEdit, 'username_lineEdit')
        self.password_lineEdit = self.findChild(QLineEdit, 'password_lineEdit')
        self.login_pushButton = self.findChild(QPushButton, 'login_pushButton')
        self.show_password_checkBox = self.findChild(QCheckBox, 'show_password_checkBox')
        self.forgot_password_commandLinkButton = self.findChild(QCommandLinkButton, 'forgot_password_commandLinkButton')

        # Mask the password
        self.password_lineEdit.setEchoMode(QLineEdit.Password)

        # Add button to show password
        self.show_password_checkBox.stateChanged.connect(self.show_password)

        # Enable the Enter button when the Enter key is pressed
        self.login_pushButton.setAutoDefault(True)
        self.password_lineEdit.returnPressed.connect(self.authentication)

        # Move cursor to password line edit when Enter key is pressed in user input
        self.username_lineEdit.returnPressed.connect(self.password_lineEdit.setFocus)

        # Set the focus to the username line edit
        self.username_lineEdit.setFocus()

        # Connect signals and slots
        self.login_pushButton.clicked.connect(self.authentication)
        self.forgot_password_commandLinkButton.clicked.connect(self.forgot_password)

        # Show the app
        self.show()

        # Disable the Enter button until a username and password are entered
        self.login_pushButton.setEnabled(False)
        self.username_lineEdit.textChanged.connect(self.enable_enter_button)
        self.password_lineEdit.textChanged.connect(self.enable_enter_button)

        # Show the app
        self.show()

    def show_password(self):
        if self.show_password_checkBox.isChecked():
            self.password_lineEdit.setEchoMode(QLineEdit.Normal)
        else:
            self.password_lineEdit.setEchoMode(QLineEdit.Password)

    # Enable the Enter button if a username and password are entered
    def enable_enter_button(self):
        if self.username_lineEdit.text() and self.password_lineEdit.text():
            self.login_pushButton.setEnabled(True)
        else:
            self.login_pushButton.setEnabled(False)

    def forgot_password(self):
        QMessageBox.information(self, "Forgot Password", "Please contact the system administrator for password recovery.  (Tel: +855 16 542 714) (Email:panhaseth453@gmail.com)")

    # Handle the authentication process
    def authentication(self):
        from admin import Admin

        username = self.username_lineEdit.text().strip()
        password = self.password_lineEdit.text().strip()

        try:
            self.user = self.db.authenticate_user(username, password)
            self.db.close_connection()
        except Exception as e:
            print(f"Error authenticating user: {e}")
            QMessageBox.warning(self, "Authentication Failed", "Failed to authenticate user.")
            return

        if self.user:
            QMessageBox.information(self, "Authentication", f"Welcome, {self.user['name']}!")
            self.admin = Admin(self.user)
            self.admin.show()
            self.close_login_page()
        else:
            QMessageBox.warning(self, "Authentication Failed", "Invalid username or password!")
    
    def close_login_page(self):
        self.close()
        self.deleteLater()

# Initialize the app
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Login()
    sys.exit(app.exec_())
