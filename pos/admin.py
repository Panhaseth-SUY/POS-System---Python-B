from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QStackedWidget, QLabel, QTableView, QLineEdit
from PyQt5 import uic
import sys
from database import Database

class admin(QMainWindow):
    def __init__(self):
        super(admin, self).__init__()
        # Initialize the database connection
        self.db = Database()

        # Load the ui file 
        uic.loadUi('ui/admin.ui', self)

        # Set the title of the window
        self.setWindowTitle("TOKATA POS System - Admin Window")
        self.showFullScreen()

        # Define our Widgets
        # Sidebar buttons
        self.dashboard_button = self.findChild(QPushButton, 'dashboard_button')
        self.categories_button = self.findChild(QPushButton, 'categories_button')
        self.products_button = self.findChild(QPushButton, 'products_button')
        self.pos_button = self.findChild(QPushButton, 'pos_button')
        self.sales_button = self.findChild(QPushButton, 'sales_button')
        self.users_button = self.findChild(QPushButton, 'users_button')
        self.setting_button = self.findChild(QPushButton, 'setting_button')
        self.signout_button = self.findChild(QPushButton, 'signout_button')

        # Dashboard widgets

        # Categories widgets

        # Products widgets
        self.products_table = self.findChild(QTableView, 'products_table')
        self.add_product_button = self.findChild(QPushButton, 'add_product_pushButton')
        self.edit_product_button = self.findChild(QPushButton, 'update_product_pushButton')
        self.export_excel_button = self.findChild(QPushButton, 'export_excel_pushButton')
        self.import_excel_button = self.findChild(QPushButton, 'import_excel_pushButton')
        self.delete_product_button = self.findChild(QPushButton, 'delete_pushButton')
        self.clear_product_button = self.findChild(QPushButton,'clear_pushButton')
        self.search_product_lineedit = self.findChild(QLineEdit,'search_product_lineEdit')
        self.search_product_button = self.findChild(QPushButton,'search_product_pushButton')

        # configuration of the products table

        
        # Handle the product buttons
        self.add_product_button.clicked.connect(self.add_product)
        self.edit_product_button.clicked.connect(self.edit_product)
        self.export_excel_button.clicked.connect(self.export_excel)
        self.import_excel_button.clicked.connect(self.import_excel)
        self.delete_product_button.clicked.connect(self.delete_product)
        self.clear_product_button.clicked.connect(self.clear_products)
        self.search_product_button.clicked.connect(self.search_product)

        # Handle the search product line edit
        self.search_product_lineedit.textChanged.connect(self.search_product)


        # POS widgets

        # Sales widgets

        # Users widgets

        # Setting widgets

        # Signout widgets



        # Label user info
        self.user_name = self.findChild(QLabel, 'user_name')
        self.user_picture = self.findChild(QLabel, 'user_picture')

        # Stacked Widget
        self.stackedWidget = self.findChild(QStackedWidget, 'stackedWidget')

        # Handle the sidebar button clicks
        self.dashboard_button.clicked.connect(self.dashboard)
        self.categories_button.clicked.connect(self.categories)
        self.products_button.clicked.connect(self.products)
        self.pos_button.clicked.connect(self.pos)
        self.sales_button.clicked.connect(self.sales)
        self.users_button.clicked.connect(self.users)
        self.setting_button.clicked.connect(self.setting)
        self.signout_button.clicked.connect(self.signout)









        # Show the app
        self.show()

    
    # Showing pages ---------------------------------------------------------------------------
    # Showing dashboard
    def dashboard(self):
        self.stackedWidget.setCurrentIndex(0)  # Change the stacked widget index to 0 (dashboard page)

    # Showing categories
    def categories(self):
        self.stackedWidget.setCurrentIndex(1)  # Change the stacked widget index to 1 (categories page)

    # Showing products
    def products(self):
        self.stackedWidget.setCurrentIndex(2)  # Change the stacked widget index to 2 (products page)

    # Showing POS
    def pos(self):
        self.stackedWidget.setCurrentIndex(3)  # Change the stacked widget index to 3 (POS page)

    # Showing sales
    def sales(self):
        self.stackedWidget.setCurrentIndex(4)  # Change the stacked widget index to 4 (sales page)

    # Showing users
    def users(self):
        self.stackedWidget.setCurrentIndex(5)  # Change the stacked widget index to 5 (users page)


    # Showing setting
    def setting(self):
        self.stackedWidget.setCurrentIndex(6) # Change the stacked widget index to 5 (setting page)

    # signout
    def signout(self):
        self.stackedWidget.setCurrentIndex(7) # Change the stacked widget index to


    # Add product --------------------------------------------------------------------------------
    def add_product(self):
        print("Add Product")
    
    # Edit product
    def edit_product(self):
        print("Edit Product")

    # Export excel
    def export_excel(self):
        print("Export Excel")

    # Import excel
    def import_excel(self):
        print("Import Excel")

    # Delete product
    def delete_product(self):
        print("Delete Product")

    # Clear products
    def clear_products(self):
        print("Clear Products")

    # Search product
    def search_product(self):
        print("Search Product")

    # Reload products
    def reload_products(self):
        print("Reload Products")








































# Initialize the app
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = admin()
    sys.exit(app.exec_())