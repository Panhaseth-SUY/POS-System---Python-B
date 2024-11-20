from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QApplication, QLineEdit, QMessageBox, QPushButton
from PyQt5 import uic
import sys
from database import Database

class Login(QMainWindow):
    def __init__(self):
        super(Login, self).__init__()
        # Load the ui file 
        uic.loadUi('ui/login.ui', self)

        # Set the title of the window
        self.setWindowTitle("Login Window")
        self.showFullScreen()

        # Define our Widgets
        self.username_lineEdit = self.findChild(QLineEdit, 'username_lineEdit')
        self.password_lineEdit = self.findChild(QLineEdit, 'password_lineEdit')
        self.enter_pushButton = self.findChild(QPushButton, 'enter_pushButton')

        # Handle the authentication process
        self.enter_pushButton.clicked.connect(self.authentication)

         # Disable the Enter button until a username and password are entered
        self.enter_pushButton.setEnabled(False)
        self.username_lineEdit.textChanged.connect(self.enable_enter_button)
        self.password_lineEdit.textChanged.connect(self.enable_enter_button)

        
        # Show the app
        self.show()

    # Enable the Enter button if a username and password are entered
    def enable_enter_button(self):
        if self.username_lineEdit.text() and self.password_lineEdit.text():
            self.enter_pushButton.setEnabled(True)
        else:
            self.enter_pushButton.setEnabled(False)

    # Handle the authentication process
    def authentication(self):
        username = self.username_lineEdit.text()
        password = self.password_lineEdit.text()

        # Authenticate the user
        db = Database()
        user = db.authenticate_user(username, password)

        if user:
            QMessageBox.information(self, "Authentication", f"Welcome, {user['name']}!")
            if user['role'] == 'admin':
                pass
            else:
                pass
        else:
            QMessageBox.warning(self, "Authentication Failed", "Invalid username or password!")

# Initialize the app
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Login()
    sys.exit(app.exec_())
