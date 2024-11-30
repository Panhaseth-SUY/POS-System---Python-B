from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QPushButton, QStackedWidget, QLabel, QTableWidget, QTableWidgetItem, QLineEdit,
    QMessageBox, QComboBox, QSpinBox, QInputDialog, QHeaderView, QAbstractItemView
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5 import uic
import sys
import pandas as pd
from database import Database
import time
from sale_report_generator import SaleReportGenerator
from add_product_dialog import AddProductDialog
from invoice_generator import InvoiceGenerator


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

        # Initialize the dashboard widget Connect signals for dashboard management
        self._initialize_dashboard_widget()
        self._connect_dashboard_signals()

        # Initialize the category widget Connect signals for category management
        self._initialize_category_widget()
        self._connect_category_signals()

        # Initialize the product widget Connect signals for product management
        self._initialize_product_widget()
        self._connect_product_signals()

        # Initialize the POS widget Connect signals for POS management
        self._intialize_pos_widgets()
        self._connect_pos_signals()

        # Initialize the sale widget Connect signals for sale management
        self._initialize_sale_widget()
        self._connect_sale_signals()

        # Initialize the user widget Connect signals for user management
        self._initialize_user_widget()
        self._connect_users_signals()

        # Set POS page as the first page in the navigation
        self._change_page(3)
        self.pos_button.setChecked(True)

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
        self.process_status_label = self.findChild(QLabel, 'process_status_Label')

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

        # Using thread to load the page
        self.thread = QThread()
        self.thread.run = lambda: self.load_page(index)
        self.thread.start()


        
    def load_page(self, index):
        # Set time wait for the page to load
        self.process_status_label.setText("Loading page...")
        if index == 0:
            self.update_dashboard_data()

        elif index == 1:
            self.reload_all_categories()

        elif index == 2:
            self.reload_all_products()

        elif index == 3:
            # Populate the pos category and product
            self.populate_pos_category()
            self.populate_pos_products()

            # reload the pos products table
            self.reload_pos_all_products()

        elif index == 4:
            # Populate the sales table
            self.reload_all_sales()

        elif index == 5:
            # Populate the users table
            self.reload_all_users()
        elif index == 6:
            pass
        else:
            pass

        self.process_status_label.setText("Page loaded successfully.")

    def signout(self):
        """Handle user signout."""
        self.close()

    def _show_error_message(self, message):
        """Display an error message to the user."""
        QMessageBox.critical(self, "Error", message)

    def _show_info_message(self, message):
        """Display an informational message to the user."""
        QMessageBox.information(self, "Information", message)



    #! Dashboard Management Functions ======================================================================
    def _initialize_dashboard_widget(self):
        # Dashboard widgets
        self.dashboard_total_sales_label = self.findChild(QLabel, 'dashboard_total_sales_label')
        self.dashboard_total_products_label = self.findChild(QLabel, 'dashboard_total_products_label')
        self.dashboard_total_users_label = self.findChild(QLabel, 'dashboard_total_users_label')
        self.dashboard_total_categories_label = self.findChild(QLabel, 'dashboard_total_categories_label')

        self.dashboard_sale_highest = self.findChild(QLabel, 'dashboard_highest_sale_label')
        self.dashboard_sale_mean = self.findChild(QLabel, 'dashboard_sale_mean_label')
        self.dashboard_sale_median = self.findChild(QLabel, 'dashboard_sale_median_label')
        self.dashboard_sale_lowest = self.findChild(QLabel, 'dashboard_sale_lowest_label')

        self.dashboard_top1_category = self.findChild(QLabel, 'dashboard_top1_categories_label')
        self.dashboard_top2_category = self.findChild(QLabel, 'dashboard_top2_categories_label')
        self.dashboard_top3_category = self.findChild(QLabel, 'dashboard_top3_categories_label')
        self.dashboard_top4_category = self.findChild(QLabel, 'dashboard_top4_categories_label')
        self.dashboard_top5_category = self.findChild(QLabel, 'dashboard_top5_categories_label')

        self.dashboard_top1_products = self.findChild(QLabel, 'dashboard_top1_product_label')
        self.dashboard_top2_products = self.findChild(QLabel, 'dashboard_top2_product_label')
        self.dashboard_top3_products = self.findChild(QLabel, 'dashboard_top3_product_label')
        self.dashboard_top4_products = self.findChild(QLabel, 'dashboard_top4_product_label')
        self.dashboard_top5_products = self.findChild(QLabel, 'dashboard_top5_product_label')

        self.dashboard_top1_users = self.findChild(QLabel, 'dashboard_top1_user_label')
        self.dashboard_top2_users = self.findChild(QLabel, 'dashboard_top2_user_label')
        self.dashboard_top3_users = self.findChild(QLabel, 'dashboard_top3_user_label')
        self.dashboard_top4_users = self.findChild(QLabel, 'dashboard_top4_user_label')
        self.dashboard_top5_users = self.findChild(QLabel, 'dashboard_top5_user_label')        

    def _connect_dashboard_signals(self):
        # Populate the dashboard with data
        self.update_dashboard_data()

    def fetch_total_numbers(self):
        total_sales = self.db.fetch_number_of_sales()
        total_products = self.db.fetch_number_of_products()
        total_users = self.db.fetch_number_of_users()
        total_categories = self.db.fetch_number_of_categories()

        self.dashboard_total_sales_label.setText(f"({str(total_sales)})")
        self.dashboard_total_products_label.setText(f"({str(total_products)})")
        self.dashboard_total_users_label.setText(f"({str(total_users)})")
        self.dashboard_total_categories_label.setText(f"({str(total_categories)})")

    def fetch_top_categories(self):
        top_categories = self.db.fetch_top_5_most_sold_categories()
        if not top_categories:
            return
        
        category_names = []
        
        # fetch categories names by category id
        for category in top_categories:
            category_names.append(self.db.fetch_category_name_by_id(category['category_id']))

        self.dashboard_top1_category.setText(str(category_names[0]))
        self.dashboard_top2_category.setText(str(category_names[1]))
        self.dashboard_top3_category.setText(str(category_names[2]))
        self.dashboard_top4_category.setText(str(category_names[3]))
        self.dashboard_top5_category.setText(str(category_names[4]))

    def fetch_top_users(self):
        top_users = self.db.fetch_top_5_most_active_users()
        if not top_users:
            return

        self.dashboard_top1_users.setText(str(top_users[0]['cashier_name']))
        self.dashboard_top2_users.setText(str(top_users[1]['cashier_name']))
        self.dashboard_top3_users.setText(str(top_users[2]['cashier_name']))
        self.dashboard_top4_users.setText(str(top_users[3]['cashier_name']))
        self.dashboard_top5_users.setText(str(top_users[4]['cashier_name']))

    def fetch_top_products(self):
        top_products = self.db.fetch_top_5_most_sold_products()
        if not top_products:
            return

        product_names = []

        # fetch product names by product id
        for product in top_products:
            product_names.append(self.db.fetch_product_name_by_id(product['product_id']))

        self.dashboard_top1_products.setText(str(product_names[0]))
        self.dashboard_top2_products.setText(str(product_names[1]))
        self.dashboard_top3_products.setText(str(product_names[2]))
        self.dashboard_top4_products.setText(str(product_names[3]))
        self.dashboard_top5_products.setText(str(product_names[4]))

    def fetch_sale_statistics(self):
        daily_sale = self.db.fetch_daily_sales_data()
        # form daily sale data find the highest, mean, median and lowest sale
        df = pd.DataFrame(daily_sale)
        highest_sale = df['total_amount'].max()
        mean_sale = df['total_amount'].mean()
        median_sale = df['total_amount'].median()
        lowest_sale = df['total_amount'].min()

        self.dashboard_sale_highest.setText(f"${highest_sale:.2f}")
        self.dashboard_sale_mean.setText(f"${mean_sale:.2f}")
        self.dashboard_sale_median.setText(f"${median_sale:.2f}")
        self.dashboard_sale_lowest.setText(f"${lowest_sale:.2f}")

    def update_dashboard_data(self):
        self.process_status_label.setText("Updating dashboard data...")
        # Update the dashboard data here
        self.fetch_total_numbers()
        self.fetch_top_categories()
        self.fetch_top_products()
        self.fetch_top_users()
        self.fetch_sale_statistics()
        self.process_status_label.setText("Dashboard data updated successfully.")
        

    #! Category Management Functions =======================================================================
    def _initialize_category_widget(self):
        # Categories widgets
        self.categories_table = self.findChild(QTableWidget, 'category_tableWidget')
        self.category_products_table = self.findChild(QTableWidget, 'category_product_tableWidget')
        self.category_products_label = self.findChild(QLabel, 'category_products_label')


        # Set the column headers for categories table
        self.categories_table.setColumnCount(5)
        self.categories_table.setHorizontalHeaderLabels(['ID', 'Name', 'Description', 'Created At', 'Updated At'])

        # Set the column headers for category products table
        self.category_products_table.setColumnCount(4)
        self.category_products_table.setHorizontalHeaderLabels(['ID', 'Name', 'Price', 'Quantity'])

        # Set the column width for categories table
        self.categories_table.setColumnWidth(0, 50)
        self.categories_table.setColumnWidth(1, 150)
        self.categories_table.setColumnWidth(2, 225)
        self.categories_table.setColumnWidth(3, 110)
        self.categories_table.setColumnWidth(4, 110)

        # Set the column width for category products table
        self.category_products_table.setColumnWidth(0, 50)
        self.category_products_table.setColumnWidth(1, 270)
        self.category_products_table.setColumnWidth(2, 110)
        self.category_products_table.setColumnWidth(3, 110)

    def _connect_category_signals(self):
        # Connect signals for category management
        self.categories_table.cellClicked.connect(lambda row, column: self.reload_category_products(self.categories_table.item(row, 0).text()))

    def reload_all_categories(self):
        self.process_status_label.setText("Reloading categories table...")
        # clear all categories
        self.categories_table.clearContents()
        self.categories_table.setRowCount(0)
        self.categories_table.setSortingEnabled(False)  # Disable sorting for performance optimization

        # Fetch all categories and populate the table
        self.categories = self.db.fetch_all_categories()

        for category in self.categories:
            row_count = self.categories_table.rowCount()
            self.categories_table.insertRow(row_count)
            self.categories_table.setItem(row_count, 0, QTableWidgetItem(str(category['id'])))
            self.categories_table.setItem(row_count, 1, QTableWidgetItem(category['name']))
            self.categories_table.setItem(row_count, 2, QTableWidgetItem(category['description']))
            self.categories_table.setItem(row_count, 3, QTableWidgetItem(category['created_at'].strftime('%Y-%m-%d %H:%M:%S')))
            self.categories_table.setItem(row_count, 4, QTableWidgetItem(category['updated_at'].strftime('%Y-%m-%d %H:%M:%S')))

        # Enable sorting after populating the table
        self.categories_table.setSortingEnabled(True)
        self.process_status_label.setText("Categories table loaded successfully.")

    def reload_category_products(self, category_id):
        self.process_status_label.setText("Reloading category products table...")
        # clear all category products
        self.category_products_table.clearContents()
        self.category_products_table.setRowCount(0)
        self.category_products_table.setSortingEnabled(False)  # Disable sorting for performance optimization

        # Fetch all category products and populate the table
        self.category_products = self.db.fetch_products_by_category(category_id)
        for product in self.category_products:
            row_count = self.category_products_table.rowCount()
            self.category_products_table.insertRow(row_count)
            self.category_products_table.setItem(row_count, 0, QTableWidgetItem(str(product['id'])))
            self.category_products_table.setItem(row_count, 1, QTableWidgetItem(product['name']))
            self.category_products_table.setItem(row_count, 2, QTableWidgetItem(f"{product['price']:.2f}"))
            self.category_products_table.setItem(row_count, 3, QTableWidgetItem(str(product['stock_quantity'])))
            self.category_products_table.setItem(row_count, 4, QTableWidgetItem(self.db.fetch_category_by_id(product['category_id'])['name']))

        # Enable sorting after populating the table
        self.category_products_table.setSortingEnabled(True)
        self.process_status_label.setText("Category products table loaded successfully.")
        self.category_products_label.setText(f"Category: {self.db.fetch_category_by_id(category_id)['name']}")



    #! Product Management Functions =======================================================================
    def _initialize_product_widget(self):
        # Products widgets
        self.products_table = self.findChild(QTableWidget, 'products_table')
        self.add_product_button = self.findChild(QPushButton, 'add_product_pushButton')
        self.update_product_button = self.findChild(QPushButton, 'update_product_pushButton')
        self.export_excel_button = self.findChild(QPushButton, 'export_excel_pushButton')
        self.import_excel_button = self.findChild(QPushButton, 'import_excel_pushButton')
        self.delete_product_button = self.findChild(QPushButton, 'delete_pushButton')
        self.reload_products_button = self.findChild(QPushButton, 'reload_pushButton')
        self.search_product_lineedit = self.findChild(QLineEdit, 'search_product_lineEdit')
        self.search_product_button = self.findChild(QPushButton, 'search_product_pushButton')

    def _connect_product_signals(self):
        # Product management
        self.add_product_button.clicked.connect(self.add_product)
        self.update_product_button.clicked.connect(self.update_product)
        self.export_excel_button.clicked.connect(self.export_excel)
        self.import_excel_button.clicked.connect(self.import_excel)
        self.delete_product_button.clicked.connect(self.delete_product)
        self.reload_products_button.clicked.connect(self.reload_all_products)
        self.search_product_button.clicked.connect(self.search_product)
        self.search_product_lineedit.textChanged.connect(self.search_product)

    def add_product(self):
        try:
            # Open the Add Product dialog
            dialog = AddProductDialog(Database=self.db)
            dialog.exec_()
            self.products = self.db.fetch_all_products()
            self.reload_all_products()
        except Exception as e:
            print(f"Error adding product: {e}")
            self._show_error_message(f"Error adding product: {e}")

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
        self.process_status_label.setText("Reloading products table...")
        # clear all products from table
        self.products_table.clearContents()
        self.products_table.setRowCount(0)

        # Set horizontal header visibility
        self.products_table.horizontalHeader().setVisible(True)

        try:
            # Define column headers
            headers = ["ID", "Name", "Stock Quantity", "Price ($)", "Category", 
                       "SKU", "Barcode", "Description", "Created At", "Updated At"]

            # Set the row and column count dynamically
            self.products_table.setRowCount(len(self.products)+28)
            self.products_table.setColumnCount(len(headers))
            self.products_table.setHorizontalHeaderLabels(headers)

            # Set the selection behavior to highlight entire rows
            self.products_table.setSelectionBehavior(QTableWidget.SelectRows)

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
                    self.process_status_label.setText("Products table loaded successfully.")
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



    #! POS Mananagement Functions =========================================================================
    def _intialize_pos_widgets(self):
        # Initialize the pos widget here
        self.pos_product_comboBox = self.findChild(QComboBox, "pos_product_comboBox")
        self.pos_quantity_spinBox = self.findChild(QSpinBox, "pos_quantity_spinBox")
        self.pos_add_to_cart_button = self.findChild(QPushButton, "pos_add_to_cart_pushButton")
        self.pos_sub_total_label = self.findChild(QLabel, "pos_sub_total_Label")
        self.pos_total_label = self.findChild(QLabel, "pos_total_Label")
        self.pos_delete_button = self.findChild(QPushButton, "pos_delete_pushButton")
        self.pos_clear_button = self.findChild(QPushButton, "pos_clear_pushButton")
        self.pos_invoice_table = self.findChild(QTableWidget, "pos_invoice_tableWidget")
        self.pos_category_comboBox = self.findChild(QComboBox, "pos_category_comboBox")
        self.pos_reload_products_table_button = self.findChild(QPushButton, "pos_reload_product_pushButton")
        self.pos_search_lineEdit = self.findChild(QLineEdit, "pos_search_lineEdit")
        self.pos_search_button = self.findChild(QPushButton, "pos_search_pushButton")
        self.pos_preview_table = self.findChild(QTableWidget, "pos_preview_tableWidget")
        self.pos_generate_invoice_button = self.findChild(QPushButton, "pos_generate_invoice_pushButton")

        # Configure invoice table
        self.pos_invoice_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.pos_invoice_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.pos_invoice_table.setColumnWidth(0, 50)
        self.pos_invoice_table.setColumnWidth(1, 235)
        self.pos_invoice_table.setColumnWidth(2, 100)
        self.pos_invoice_table.setColumnWidth(3, 80)
        self.pos_invoice_table.setColumnWidth(4, 120)

    def _connect_pos_signals(self):
        # Connect signals for the pos management
        self.pos_add_to_cart_button.clicked.connect(self.add_product_to_cart)
        self.pos_delete_button.clicked.connect(self.delete_product_from_cart)
        self.pos_clear_button.clicked.connect(self.clear_cart)
        self.pos_search_button.clicked.connect(self.pos_search_product)
        self.pos_search_lineEdit.textChanged.connect(self.pos_search_product)
        self.pos_category_comboBox.currentIndexChanged.connect(self.filter_product_by_category)
        self.pos_reload_products_table_button.clicked.connect(self.reload_pos_all_products)
        self.pos_invoice_table.cellDoubleClicked.connect(lambda row, col: self.edit_quantity(row, col))
        self.pos_generate_invoice_button.clicked.connect(self.generate_invoice)

    def populate_pos_category(self):
        # Populate the pos category combo box with data from the database
        self.pos_category_comboBox.clear()

        try:
            categories = self.db.fetch_all_categories()
            self.pos_category_comboBox.addItem("All Categories", 0)  # Add an "All Categories" option at the top
            for category in categories:
                self.pos_category_comboBox.addItem(category['name'], category['id'])
        except Exception as e:
            print(f"Error loading categories: {e}")
            self._show_error_message("Failed to load categories.")

    def populate_pos_products(self):
        # Populate the pos product combo box with data from the database
        self.pos_product_comboBox.clear()

        try:
            products = self.db.fetch_all_products()
            for product in products:
                self.pos_product_comboBox.addItem(product['name'], product['id'])
        except Exception as e:
            print(f"Error loading products: {e}")
            self._show_error_message("Failed to load products.")
        
    def add_product_to_cart(self):
        product_id = self.pos_product_comboBox.currentData()  # Retrieve the selected product ID
        quantity = self.pos_quantity_spinBox.value()         # Retrieve the quantity from spin box

        if product_id is None or quantity <= 0:
            self._show_error_message("Invalid product or quantity.")
            return

        # Validate product quantity
        stock_quantity = self.db.fetch_product_stock_quantity_by_id(product_id)
        current_quantity_in_cart = 0
        for row in range(self.pos_invoice_table.rowCount()):
            if self.pos_invoice_table.item(row, 0).text() == str(product_id):
                current_quantity_in_cart += int(self.pos_invoice_table.item(row, 3).text())
        
        if stock_quantity < quantity + current_quantity_in_cart:
            self._show_error_message(f"Not enough stock. Only {stock_quantity} available.")
            return

        try:
            product_details = self.db.fetch_product_by_id(product_id)
            if product_details:
                # Add product details and quantity to the invoice table
                row_count = self.pos_invoice_table.rowCount()
                self.pos_invoice_table.insertRow(row_count)
                self.pos_invoice_table.setItem(row_count, 0, QTableWidgetItem(str(product_id)))
                self.pos_invoice_table.setItem(row_count, 1, QTableWidgetItem(product_details['name']))
                self.pos_invoice_table.setItem(row_count, 2, QTableWidgetItem(str(product_details['price'])))
                self.pos_invoice_table.setItem(row_count, 3, QTableWidgetItem(str(quantity)))
                self.pos_invoice_table.setItem(row_count, 4, QTableWidgetItem(str(quantity * product_details['price'])))
                self.update_totals()
                self.combine_duplicates()
            else:
                self._show_error_message("Product not found.")
        except Exception as e:
            print(f"Error adding product to cart: {e}")
            self._show_error_message("Failed to add product to cart.")
        finally:
            self.pos_quantity_spinBox.setValue(1)  # Reset the quantity spin box

    def update_totals(self):
        self.total = 0
        for row in range(self.pos_invoice_table.rowCount()):
            price = float(self.pos_invoice_table.item(row, 2).text())
            quantity = int(self.pos_invoice_table.item(row, 3).text())
            self.total += price * quantity
        self.pos_total_label.setText(f"Total:          ${self.total:.2f}")
        self.pos_sub_total_label.setText(f"Sub Total:  ${self.total:.2f}")
        font = self.pos_total_label.font()
        font.setPointSize(14)
        self.pos_total_label.setFont(font)
        self.pos_sub_total_label.setFont(font)

    def delete_product_from_cart(self):
        selected_row = self.pos_invoice_table.currentRow()
        if selected_row < 0:
            self._show_error_message("No selected product.")
            return

        self.pos_invoice_table.removeRow(selected_row)
        self.update_totals()

    def clear_cart(self):
        self.pos_invoice_table.clearContents()
        self.pos_invoice_table.setRowCount(0)
        self.update_totals()

    def reload_pos_products_table(self):
        # Reload the POS products table here
        self.process_status_label.setText("Reloading POS products table...")
        self.pos_preview_table.clearContents()
        self.pos_preview_table.setRowCount(0)

        # Set horizontal header visibility
        self.pos_preview_table.horizontalHeader().setVisible(True)

        # Set the column headers
        self.pos_preview_table.setColumnCount(6)
        self.pos_preview_table.setHorizontalHeaderLabels(["ID", "Name", "Price ($)", "Categories", "Quantity", "Description"])

        product = self.pos_products

        # Populate the table with data from the database
        try:
            self.pos_preview_table.setRowCount(len(product))
            self.pos_preview_table.setSortingEnabled(False)

            for row_index, product in enumerate(product):
                self.pos_preview_table.setItem(row_index, 0, QTableWidgetItem(str(product['id'])))
                self.pos_preview_table.setItem(row_index, 1, QTableWidgetItem(product['name']))
                self.pos_preview_table.setItem(row_index, 2, QTableWidgetItem(f"{product['price']:.2f}"))
                category = self.db.fetch_category_by_id(product['category_id'])
                self.pos_preview_table.setItem(row_index, 3, QTableWidgetItem(category['name']))
                self.pos_preview_table.setItem(row_index, 4, QTableWidgetItem(str(product['stock_quantity'])))
                self.pos_preview_table.setItem(row_index, 5, QTableWidgetItem(product['description']))            

            # set column to fit with table width
            self.pos_preview_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

            # set column width to fit with table width
            self.pos_preview_table.setSelectionBehavior(QTableWidget.SelectRows)
            self.pos_preview_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.pos_preview_table.setSortingEnabled(True)
            self.process_status_label.setText("POS products table reloaded successfully.")    

        except Exception as e:
            print(f"Error reloading POS products table: {e}")
            self._show_error_message("Failed to reload POS products table.")
            self.process_status_label.setText("")

    def reload_pos_all_products(self):
        # Reload all products in the POS products table
        self.pos_category_comboBox.setCurrentIndex(0)
        self.pos_products = self.db.fetch_all_products()
        self.reload_pos_products_table()

    def filter_product_by_category(self):
        # Filter products by category in the POS products table
        category_id = self.pos_category_comboBox.currentData()
        if category_id == 0:
            self.pos_products = self.db.fetch_all_products()
        else:
            self.pos_products = self.db.fetch_products_by_category(category_id)
        self.reload_pos_products_table()

    def pos_search_product(self):
        # Search for a product in the POS products table
        search_term = self.pos_search_lineEdit.text().strip().lower()
        try:
            if search_term:
                self.pos_products = self.db.search_products_by_name(search_term)
            else:
                self.pos_products = self.db.fetch_all_products()
            self.reload_pos_products_table()
        except Exception as e:
            print(f"Error searching products: {e}")
            self._show_error_message("Failed to search products")
            self.pos_search_lineEdit.clear()

    # Edit quantity field in invoice table
    def edit_quantity(self, row, column):
        if column == 3:
            current_quantity = int(self.pos_invoice_table.item(row, column).text())
            quantity, ok = QInputDialog.getInt(self, "Edit Quantity", "Enter new quantity:", value=current_quantity)
            if ok:
                self.pos_invoice_table.setItem(row, column, QTableWidgetItem(str(quantity)))
                self.update_totals()

    # Combine duplicates in the invoice table
    def combine_duplicates(self):
        for row in range(self.pos_invoice_table.rowCount()):
            for row2 in range(row+1, self.pos_invoice_table.rowCount()):
                if self.pos_invoice_table.item(row, 0).text() == self.pos_invoice_table.item(row2, 0).text():
                    quantity = int(self.pos_invoice_table.item(row, 3).text()) + int(self.pos_invoice_table.item(row2, 3).text())
                    self.pos_invoice_table.setItem(row, 3, QTableWidgetItem(str(quantity)))
                    self.pos_invoice_table.removeRow(row2)
                    self.update_totals()

    def generate_invoice(self):
        # Generate the invoice here
        if self.pos_invoice_table.rowCount() == 0:
            self._show_error_message("No products in the cart.")
            return

        try:
            total = self.total
            cashier_id = 1
            cashier_name = self.db.fetch_user_by_id(cashier_id)
            cashier_name = cashier_name['name']

            # Get payment method
            payment_methods = ["Cash", "Card", "Digital Wallet"]
            payment_method, ok = QInputDialog.getItem(self, "Payment Method", "Select payment method:", payment_methods, 0, False)
            if not ok:
                self._show_error_message("Payment method selection cancelled.")
                return
            
            # save sales order to database
            self.db.add_sale(total, cashier_id, cashier_name, payment_method)

            # save sales items to database
            sale_id = self.db.get_last_sale_id()

            for row in range(self.pos_invoice_table.rowCount()):
                product_id = self.pos_invoice_table.item(row, 0).text()
                quantity = int(self.pos_invoice_table.item(row, 3).text())
                price = float(self.pos_invoice_table.item(row, 2).text())
                sub_total = float(self.pos_invoice_table.item(row, 4).text())
                self.db.add_sale_item(sale_id, product_id, quantity, price, sub_total)

                # Update stock
                current_stock = self.db.fetch_product_stock_quantity_by_id(product_id)
                new_stock = current_stock - quantity
                self.db.update_product(product_id=product_id, stock_quantity=new_stock)

            # Invoice PDF generation
            invoice_generator = InvoiceGenerator(Database=self.db)
            invoice_file_path = invoice_generator.generate()

            # Preview PDF generation
            # self.preview_pdf_invoice(invoice_file_path)

            # Clear the cart and update totals
            self.clear_cart()
            self.update_totals()

            # Reload the products table
            self.filter_product_by_category()

            self.process_status_label.setText("Invoice generated successfully.")
            self._show_info_message("Invoice generated successfully.")
        except Exception as e:
            print(f"Error generating invoice: {e}")
            self._show_error_message("Failed to generate invoice.")
            self.process_status_label.setText("Failed to generate invoice.")


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
        self.search_sale_button.clicked.connect(self.search_sales)
        self.search_sale_lineedit.textChanged.connect(self.search_sales)

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

        if not cashier_name:
            cashier_name = self.db.fetch_user_by_id(cashier_id)
            cashier_name = cashier_name['name']

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
            SaleReportGenerator(date_start="2015-01-01", date_end="2023-12-31", Database=self.db)
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
        self.process_status_label.setText("Reloading sales table...")
        self.sales_table.clearContents()
        self.sales_table.setRowCount(0)
        
        # set horizontal header visibility
        self.sales_table.horizontalHeader().setVisible(True)

        # Set the column headers
        self.sales_table.setColumnCount(8)
        self.sales_table.setHorizontalHeaderLabels(["ID", "Date", "Total Amount ($)", "Cashier ID", 
                                                    "Cashier Name", "Payment Method", "Status", "Date Edited"])
        
        sales_data = self.sales
        self.sales_table.setRowCount(len(sales_data)+28)
        self.sales_table.setSortingEnabled(False)

        # Populate table with sales data
        for row_index, sale in enumerate(sales_data):
            self.sales_table.setItem(row_index, 0, QTableWidgetItem(str(sale['id'])))
            self.sales_table.setItem(row_index, 1, QTableWidgetItem(sale['date'].strftime('%Y-%m-%d %H:%M:%S')))
            self.sales_table.setItem(row_index, 2, QTableWidgetItem(f"{sale['total_amount']:.2f}"))
            self.sales_table.setItem(row_index, 3, QTableWidgetItem(str(sale['cashier_id'])))
            self.sales_table.setItem(row_index, 4, QTableWidgetItem(sale['cashier_name']))
            self.sales_table.setItem(row_index, 5, QTableWidgetItem(sale['payment_method']))
            self.sales_table.setItem(row_index, 6, QTableWidgetItem(sale['status']))
            self.sales_table.setItem(row_index, 7, QTableWidgetItem(sale['updated_at'].strftime('%Y-%m-%d %H:%M:%S')))


        # Columns to make non-editable (e.g., ID, Updated At)
        non_editable_columns = {0, 1, 7}

        # Populate the table with data
        for row_index, sale in enumerate(self.sales):
            for col_index, value in enumerate([
                str(sale['id']),  # Sale ID
                sale['date'].strftime('%Y-%m-%d %H:%M:%S'),  # Date
                f"{sale['total_amount']:.2f}",  # Total Amount
                str(sale['cashier_id']),  # Cashier ID
                sale['cashier_name'],  # Cashier Name
                sale['payment_method'],  # Payment Method
                sale['status'],  # Status
                sale['updated_at'].strftime('%Y-%m-%d %H:%M:%S'),  # Updated At
            ]):
                # Create a QTableWidgetItem for each value
                item = QTableWidgetItem(value)

                # Disable editing for specified columns
                if col_index in non_editable_columns:
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # Non-editable

                # Set the item in the sales table
                self.sales_table.setItem(row_index, col_index, item)


                # set column width to fit with table width
                self.sales_table.horizontalHeader().setSectionResizeMode(1)
                self.sales_table.setSelectionBehavior(QTableWidget.SelectRows)
                self.sales_table.setSortingEnabled(True)

    def reload_all_sales(self):
        self.sales = self.db.fetch_all_sales()
        self.reload_sales_table() 

    def search_sales(self):
        search_term = self.search_sale_lineedit.text().strip().lower()
        try:
            if search_term:
                self.sales = self.db.search_sales_by_cashier_name(search_term)
            else:
                self.sales = self.db.fetch_all_sales()
            self.reload_sales_table()
        except Exception as e:
            print(f"Error searching sales: {e}")
            self._show_error_message("Failed to search sales.")



    #! User Management Functions ===========================================================================
    def _initialize_user_widget(self):
        # Initialize the user widget here
        self.users_table = self.findChild(QTableWidget, 'users_tableWidget')

        # Set the column headers
        self.users_table.setColumnCount(8)
        self.users_table.setHorizontalHeaderLabels(["ID", "Name", "Role", "Username", "Password", "Status", "Created At", "Updated At"])

    def _connect_users_signals(self):
        # Connect signals for user management
        pass

    def reload_users_table(self):
        self.process_status_label.setText("Reloading users table...")
        self.users_table.clearContents()
        self.users_table.setRowCount(0)
        
        # Set horizontal header visibility
        self.users_table.horizontalHeader().setVisible(True)

        # Populate table with user data
        users_data = self.users
        self.users_table.setRowCount(len(users_data))

        # Populate the table with data
        for row_index, user in enumerate(users_data):
            self.users_table.setItem(row_index, 0, QTableWidgetItem(str(user['id'])))
            self.users_table.setItem(row_index, 1, QTableWidgetItem(user['name']))
            self.users_table.setItem(row_index, 2, QTableWidgetItem(user['role']))
            self.users_table.setItem(row_index, 3, QTableWidgetItem(user['username']))
            self.users_table.setItem(row_index, 4, QTableWidgetItem(user['password']))
            self.users_table.setItem(row_index, 5, QTableWidgetItem(user['status']))
            self.users_table.setItem(row_index, 6, QTableWidgetItem(user['created_at'].strftime('%Y-%m-%d %H:%M:%S')))
            self.users_table.setItem(row_index, 7, QTableWidgetItem(user['updated_at'].strftime('%Y-%m-%d %H:%M:%S')))

        # Columns to make non-editable (e.g., ID, Updated At)
        non_editable_columns = {0, 6, 7}

        # Populate the table with data
        for row_index, user in enumerate(self.users):
            for col_index, value in enumerate([
                str(user['id']),  # User ID
                user['name'],  # Name
                user['role'],  # Role
                user['username'],  # Username
                user['password'],  # Password
                user['status'],  # Status
                user['created_at'].strftime('%Y-%m-%d %H:%M:%S'),  # Created At
                user['updated_at'].strftime('%Y-%m-%d %H:%M:%S'),  # Updated At
            ]):
                # Create a QTableWidgetItem for each value
                item = QTableWidgetItem(value)

                # Disable editing for specified columns
                if col_index in non_editable_columns:
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

                # Set the item in the users table
                self.users_table.setItem(row_index, col_index, item)

        # set column width to fit with table width
        self.users_table.horizontalHeader().setSectionResizeMode(1)
        self.users_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.users_table.setSortingEnabled(True)
        self.process_status_label.setText("Users table reloaded.")

    def reload_all_users(self):
        self.users = self.db.fetch_all_users()
        self.reload_users_table()

class PageLoaderThread(QThread):
    progress_signal = pyqtSignal(str)  # Signal to send progress updates
    error_signal = pyqtSignal(str)     # Signal to notify errors
    finished_signal = pyqtSignal()    # Signal to notify successful completion

    def __init__(self, index, parent=None):
        super().__init__(parent)
        self.index = index

    def run(self):
        try:
            for i in range(5):  # Simulate a page-loading task
                time.sleep(1)  # Simulate delay
                self.progress_signal.emit(f"Loading step {i + 1}/5 for page {self.index}")
            self.finished_signal.emit()
        except Exception as e:
            self.error_signal.emit(str(e))

# TODO: Run Admin Page
if __name__ == "__main__":
    app = QApplication(sys.argv)
    admin_window = Admin()
    sys.exit(app.exec_())
