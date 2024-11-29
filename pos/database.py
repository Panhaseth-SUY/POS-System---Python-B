import hashlib
import mysql.connector
import pandas as pd
from PyQt5.QtWidgets import QApplication, QFileDialog
import datetime
class Database:
    def __init__(self, host="127.0.0.1", username="root", password="Tokata@se7en232722", database="POS_DB"):
        self.host = host
        self.username = username
        self.password = password
        self.database = database

        self.conn = None
        self.cursor = None

        self.connect_db()

    # Connect to the database (Establish self.conn with database).
    def connect_db(self):
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.username,
                password=self.password,
                database=self.database
            )
            print("--> Database connection established successfully!")
        except mysql.connector.Error as e:
            raise Exception(f"Database connection failed: {e}")

    # Execute a query (return result if fetch=True, fetchone=True, or None)
    def execute_query(self, query, params=None, fetchall=False, fetchone=False):
        # Check if the database connection is established or not.
        if not self.conn:
            self.connect_db()
        
        try:
            self.cursor = self.conn.cursor(dictionary=True)
            # Execute query with or without parameters
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            
            # Handle fetching data for SELECT queries
            if fetchall:
                return self.cursor.fetchall()
            elif fetchone:
                return self.cursor.fetchone()
            
            # Commit changes for non-SELECT queries
            self.conn.commit()
        except mysql.connector.Error as e:
            raise Exception(f"Query execution failed: {e}")
        finally:
            # Ensure cursor is always closed after execution
            if self.cursor:
                self.cursor.close()

    # Initialize all tables for database
    def initialize_tables(self):
        queries = [
            """CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            username VARCHAR(50) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL, 
            role ENUM('Admin', 'Cashier', 'Manager') NOT NULL DEFAULT 'Cashier',
            status ENUM('Active', 'Inactive') NOT NULL DEFAULT 'Active', 
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )""",

            """CREATE TABLE IF NOT EXISTS categories (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL UNIQUE,
            description TEXT,
            isDeleted BOOLEAN NOT NULL DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )""",

            """CREATE TABLE IF NOT EXISTS products (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            category_id INT NOT NULL,
            sku VARCHAR(50) NOT NULL UNIQUE,
            barcode VARCHAR(50) NOT NULL UNIQUE,
            description TEXT,
            price DECIMAL(10, 2) NOT NULL CHECK(price >= 0),
            stock_quantity INT NOT NULL CHECK(stock_quantity >= 0),
            isDeleted BOOLEAN NOT NULL DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
            )""",

            """CREATE TABLE IF NOT EXISTS sales (
            id INT AUTO_INCREMENT PRIMARY KEY,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            total_amount DECIMAL(10, 2) NOT NULL CHECK(total_amount >= 0),
            cashier_id INT NOT NULL,
            cashier_name VARCHAR(255),
            payment_method ENUM('Cash', 'Card', 'Digital Wallet') NOT NULL,
            status ENUM('Completed', 'Pending', 'Canceled') DEFAULT 'Completed',
            isDeleted BOOLEAN NOT NULL DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (cashier_id) REFERENCES users(id)
            )""",

            """CREATE TABLE IF NOT EXISTS sales_items (
            id INT AUTO_INCREMENT PRIMARY KEY,
            sale_id INT,
            product_id INT,
            quantity INT NOT NULL,
            unit_price DECIMAL(10, 2) NOT NULL CHECK (unit_price >= 0),
            subtotal DECIMAL(10, 2) NOT NULL CHECK (subtotal >= 0), 
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (sale_id) REFERENCES sales(id) ON DELETE CASCADE,
            FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
            )""",
        ]
        try:
            for query in queries:
                self.execute_query(query)
            print("--> All Tables are initialized successfully!")
        except Exception as e:
            print(f"--> Error initializing tables: {e}")





    #! Add a user -----------------------------------------------------
    def add_user(self, name, username, password, role):
        hash_password = self.hash_password(password)
        query = "INSERT INTO users(name, username, password, role) VALUES(%s, %s, %s, %s)"
        params = (name, username, hash_password, role)
        try:
            self.execute_query(query, params)
            print(f"-->{name} ({role}) has been added into the database successfully!")
        except Exception as e:
            print(f"--> Error inserting user: {e}")

    # Fetch all users
    def fetch_all_users(self):
        query = "SELECT * FROM users"
        try:
            results = self.execute_query(query, fetchall=True)
            return results
        except Exception as e:
            print(f"--> Error fetching users: {e}")
            return None

    # fetch a user by id
    def fetch_user_by_id(self, user_id):
        query = "SELECT * FROM users WHERE id=%s"
        params = (user_id,)
        try:
            result = self.execute_query(query, params, fetchone=True)
            return result
        except Exception as e:
            print(f"--> Error fetching user by ID: {e}")
            return None

    # Fetch a user by username
    def fetch_user_by_username(self, username):
        query = "SELECT * FROM users WHERE username=%s"
        params = (username,)
        try:
            result = self.execute_query(query, params, fetchone=True)
            return result
        except Exception as e:
            print(f"--> Error fetching user by username: {e}")
            return None
        
    # Update a user
    def update_user(self, username=None, name=None, password=None, role=None, status=None):
        query = "UPDATE users SET "
        params = []
        if name:
            query += "name=%s, "
            params.append(name)
        if password:
            query += "password=%s, "
            params.append(self.hash_password(password))
        if role:
            query += "role=%s, "
            params.append(role)
        if status:
            query += "status=%s, "
            params.append(status)

        query = query.rstrip(", ") + " WHERE username=%s"
        params.append(username)

        try:
            self.execute_query(query, params)
            print(f"-->{username} has been updated successfully!")
        except Exception as e:
            print(f"--> Error updating user: {e}")

    # Delete a user
    def delete_user(self, username):
        query = "DELETE FROM users WHERE username=%s"
        params = (username,)
        try:
            self.execute_query(query, params)
            print(f"-->{username} has been deleted successfully!")
        except Exception as e:
            print(f"--> Error deleting user: {e}")

    # Clear all users except admin
    def clear_all_users(self):
        query = "DELETE FROM users WHERE role!='admin'"
        try:
            self.execute_query(query)
            print("--> All users except admin have been cleared successfully!")
        except Exception as e:
            print(f"--> Error clearing users: {e}")

    # Authenticate
    def authenticate_user(self, username, password):
        hash_password = self.hash_password(password)
        query = "SELECT * FROM users WHERE username=%s AND password=%s"
        params = (username, hash_password)
        try:
            result = self.execute_query(query, params, fetchone=True)
            # check user status
            if result and result["status"] == "Active":
                return result
            else:
                print("--> Invalid credentials or user status is not active.")
                return False
        except Exception as e:
            print(f"--> Error authenticating user: {e}")
            return False

    # Hash a password
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()






    #! Add a product ----------------------------------------------------------------
    def add_product(self, name, sku, barcode, description, price, stock_quantity, category_id):
        query = "INSERT INTO products(name, sku, barcode, description, price, stock_quantity, category_id) VALUES(%s, %s, %s, %s, %s, %s, %s)"
        params = (name, sku, barcode, description, price, stock_quantity, category_id)
        try:
            self.execute_query(query, params)
            print(f"-->Product: ({name}) has been added into the database successfully!")
        except Exception as e:
            print(f"--> Error inserting product: {e}")

    # Add products from dataset (csv, excel)
    def add_products_from_dataset(self):
        # Ask the user to select a dataset file
        options = QFileDialog.Options()
        dataset, _ = QFileDialog.getOpenFileName(None, "Select Dataset", "", "CSV Files (*.csv);;Excel Files (*.xlsx)", options=options)
        
        # Check for file type
        if dataset.endswith(".csv"):
            try:
                data = pd.read_csv(dataset)
                for index, row in data.iterrows():
                    # Get category id
                    category = self.fetch_category_by_name(row["category_name"])
                    if category:
                        category_id = category["id"]
                        self.add_product(row["name"], row["sku"], row["barcode"], row.get("description", None), row["price"], row["stock_quantity"], category_id)
            except Exception as e:
                print(f"--> Error adding products from dataset: {e}")

        elif dataset.endswith(".xlsx"):
            try:
                data = pd.read_excel(dataset)
                for index, row in data.iterrows():
                    # Get category id
                    category = self.fetch_category_by_name(row["category_name"])
                    if category:
                        category_id = category["id"]
                        self.add_product(row["name"], row["sku"], row["barcode"], row.get("description", None), row["price"], row["stock_quantity"], category_id)
            except Exception as e:
                print(f"--> Error adding products from dataset: {e}")
        else:
            print("--> Invalid file type. Only csv, and excel files are supported.")
            raise Exception

    # Fetch all products
    def fetch_all_products(self):
        query = "SELECT * FROM products WHERE isDeleted = False"
        try:
            results = self.execute_query(query, fetchall=True)
            return results
        except Exception as e:
            print(f"--> Error fetching products: {e}")
            return None

    # Save products table to excel file
    def save_products_table_as_excel_file(self):
        query1 = "SELECT * FROM products"
        query2 = "SELECT * FROM categories"
        try:
            result1 = self.execute_query(query1, fetchall=True)
            result2 = self.execute_query(query2, fetchall=True)
            products = pd.DataFrame(result1)
            categories = pd.DataFrame(result2)

            # Drop unnecessary columns
            products.drop(['created_at', 'updated_at'], axis=1, inplace=True)
            categories.drop(['created_at', 'updated_at', 'description'], axis=1, inplace=True)

            # Rename the category
            categories.rename(columns={'id': 'category_id', 'name': 'category_name'}, inplace=True)

            # Merge products and categories
            excel = pd.merge(products, categories, on='category_id', how='left')

            # Reorder the category columns
            excel = excel[['id', 'name', 'sku', 'barcode', 'price', 'stock_quantity', 'category_name', 'description']]

            # Ask the user for the file path and name to save the Excel file
            options = QFileDialog.Options()
            filename, _ = QFileDialog.getSaveFileName(None, "Save Excel File", "", "Excel files (*.xlsx)", options=options)

            # Save the dataframe to the Excel file
            excel.to_excel(filename, index=False)
            print("--> Products table has been saved to excel successfully!")
        except Exception as e:
            print(f"--> Error saving products to excel: {e}")
            raise Exception
        
    # Search products by name
    def search_products_by_name(self, name):
        query = "SELECT * FROM products WHERE isDeleted=False AND name LIKE %s"
        params = (f"%{name}%",)
        try:
            results = self.execute_query(query, params, fetchall=True)
            return results
        except Exception as e:
            print(f"--> Error searching products by name: {e}")
            return None

    # Fetch a product by ID
    def fetch_product_by_id(self, product_id):
        query = "SELECT * FROM products WHERE isDeleted=False AND id=%s"
        params = (product_id,)
        try:
            result = self.execute_query(query, params, fetchone=True)
            return result
        except Exception as e:
            print(f"--> Error fetching product by ID: {e}")
            return None

    # Update a product
    def update_product(self, product_id, name=None, sku=None, barcode=None, description=None, price=None, stock_quantity=None, category_id=None):
        query = "UPDATE products SET "
        params = []

        if name:
            query += "name=%s, "
            params.append(name)
        if sku:
            query += "sku=%s, "
            params.append(sku)
        if barcode:
            query += "barcode=%s, "
            params.append(barcode)
        if description:
            query += "description=%s, "
            params.append(description)
        if price:
            query += "price=%s, "
            params.append(price)
        if stock_quantity:
            query += "stock_quantity=%s, "
            params.append(stock_quantity)
        if category_id:
            query += "category_id=%s "
            params.append(category_id)

        query = query.rstrip(", ") + " WHERE id=%s"
        params.append(product_id)

        try:
            self.execute_query(query, params)
            print(f"-->Product: ({name}) has been updated successfully!")
        except Exception as e:
            print(f"--> Error updating product: {e}")

    # Delete a product
    def delete_product(self, product_id):
        query = "DELETE FROM products WHERE id=%s"
        params = (product_id,)
        try:
            self.execute_query(query, params)
            print(f"-->Product: ({product_id}) has been deleted successfully!")
        except Exception as e:
            print(f"--> Error deleting product: {e}")

    # soft delete a product
    def soft_delete_product(self, product_id):
        query = "UPDATE products SET isDeleted=True WHERE id=%s"
        params = (product_id,)
        try:
            self.execute_query(query, params)
            print(f"--> Product: ({product_id}) has been soft deleted successfully!")
        except Exception as e:
            print(f"--> Error soft deleting product: {e}")

    # Clear all products
    def soft_clear_products(self):
        query = "UPDATE products SET isDeleted=True"
        try:
            self.execute_query(query)
            print("--> All products have been soft deleted successfully!")
        except Exception as e:
            print(f"--> Error soft deleting all products: {e}")
            raise Exception

    # Clear all products
    def clear_all_products(self):
        query = "DELETE FROM products"
        try:
            self.execute_query(query)
            print("--> All products have been cleared successfully!")
        except Exception as e:
            print(f"--> Error clearing products: {e}")
            
    # Check if a product if it is referenced in the sales_items table
    def is_product_referenced(self, product_id):
        query = "SELECT COUNT(*) as count FROM sales_items WHERE product_id = %s"
        params = (product_id,)
        try:
            result = self.execute_query(query, params, fetchone=True)
            return result['count'] > 0
        except Exception as e:
            print(f"--> Error checking if product is referenced: {e}")
            return False


    #! Add a category --------------------------------------------------------------
    def add_category(self, name, description=None):
        query = "INSERT INTO categories(name, description) VALUES(%s, %s)"
        params = (name, description)
        try:
            self.execute_query(query, params)
            print(f"-->Category: ({name}) has been added into the database successfully!")
        except Exception as e:
            print(f"--> Error inserting category: {e}")

    # Add categories from dataset (csv, excel)
    def add_categories_from_dataset(self):
        # Ask the user to select a dataset file
        app = QApplication([])
        options = QFileDialog.Options()
        dataset, _ = QFileDialog.getOpenFileName(None, "Select Dataset", "", "CSV Files (*.csv);;Excel Files (*.xlsx)", options=options)
        app.exit()
        
        # Check for file type
        if dataset.endswith(".csv"):
            try:
                data = pd.read_csv(dataset)
                for index, row in data.iterrows():
                    self.add_category(row["name"], row.get("description", None))
            except Exception as e:
                print(f"--> Error adding categories from dataset: {e}")
                
        elif dataset.endswith(".xlsx"):
            try:
                data = pd.read_excel(dataset)
                for index, row in data.iterrows():
                    self.add_category(row["name"], row.get("description", None))
            except Exception as e:
                print(f"--> Error adding categories from dataset: {e}")
        else:
            print("--> Invalid file type. Only csv, and excel files are supported.")

    # Fetch all categories
    def fetch_all_categories(self):
        query = "SELECT * FROM categories WHERE isDeleted=False"
        try:
            results = self.execute_query(query, fetchall=True)
            return results
        except Exception as e:
            print(f"--> Error fetching categories: {e}")
            return None
        
    # Fetch a category by ID
    def fetch_category_by_id(self, category_id):
        query = "SELECT * FROM categories WHERE isDeleted=False AND id=%s"
        params = (category_id,)
        try:
            result = self.execute_query(query, params, fetchone=True)
            return result
        except Exception as e:
            print(f"--> Error fetching category by ID: {e}")
            return None

    # Fetch a category by name
    def fetch_category_by_name(self, name):
        query = "SELECT * FROM categories WHERE isDeleted=False AND name=%s"
        params = (name,)
        try:
            result = self.execute_query(query, params, fetchone=True)
            return result
        except Exception as e:
            print(f"--> Error fetching category by name: {e}")
            return None

    # Update a category
    def update_category(self, category_id, name, description=None):
        query = "UPDATE categories SET name=%s"
        params = [name]

        if description:
            query += ", description=%s"
            params.append(description)

        query += " WHERE id=%s"
        params.append(category_id)

        try:
            self.execute_query(query, params)
            print(f"-->Category: ({name}) has been updated successfully!")
        except Exception as e:
            print(f"--> Error updating category: {e}")

    # Delete a category
    def delete_category(self, category_id):
        query = "DELETE FROM categories WHERE id=%s"
        params = (category_id,)
        try:
            self.execute_query(query, params)
            print(f"-->Category: ({category_id}) has been deleted successfully!")
        except Exception as e:
            print(f"--> Error deleting category: {e}")

    # soft delete a category
    def soft_delete_category(self, category_id):
        query = "UPDATE categories SET isDeleted=True WHERE id=%s"
        params = (category_id,)
        try:
            self.execute_query(query, params)
            print(f"--> Category: ({category_id}) has been soft deleted successfully!")
        except Exception as e:
            print(f"--> Error soft deleting category: {e}")

    # Clear all categories
    def clear_all_categories(self):
        query = "DELETE FROM categories"
        try:
            self.execute_query(query)
            print("--> All categories have been cleared successfully!")
        except Exception as e:
            print(f"--> Error clearing categories: {e}")





    #! Add a sale --------------------------------------------------------------
    def add_sale(self, total_amount, cashier_id, cashier_name, payment_method, date=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')):
        query = "INSERT INTO sales(date, total_amount, cashier_id, cashier_name, payment_method) VALUES(%s, %s, %s, %s, %s)"
        params = (date, total_amount, cashier_id, cashier_name, payment_method)
        try:
            self.execute_query(query, params)
            # get last sale id from the database
            sale_id = self.get_last_sale_id()

            print(f"-->Sale({sale_id}) by cashier({cashier_id}) has been added into the database successfully!")
        except Exception as e:
           print(f"--> Error inserting sale: {e}")

    # Add sales from dataset (csv, excel)
    def add_sales_from_dataset(self):
        # Ask the user to select a dataset file
        options = QFileDialog.Options()
        dataset, _ = QFileDialog.getOpenFileName(None, "Select Dataset", "", "CSV Files (*.csv);;Excel Files (*.xlsx)", options=options)

        # Check for file type
        if dataset.endswith(".csv"):
            try:
                data = pd.read_csv(dataset)
                for index, row in data.iterrows():
                    self.add_sale(row["total_amount"], row["cashier_id"], row["payment_method"], row["date"])
            except Exception as e:
                print(f"--> Error adding sales from dataset: {e}")
                
        elif dataset.endswith(".xlsx"):
            try:
                data = pd.read_excel(dataset)
                for index, row in data.iterrows():
                    self.add_sale(row["total_amount"], row["cashier_id"], row["payment_method"], row["date"])
            except Exception as e:
                print(f"--> Error adding sales from dataset: {e}")
        else:
            print("--> Invalid file type. Only csv, and excel files are supported.")           

    # Get last sale id 
    def get_last_sale_id(self):
        query = "SELECT id FROM sales ORDER BY id DESC LIMIT 1"
        try:
            result = self.execute_query(query, fetchone=True)
            return result["id"]
        except Exception as e:
            print(f"--> Error fetching last sale id: {e}")
            return None

    # Fetch all sales
    def fetch_all_sales(self):
        query = "SELECT * FROM sales"
        try:
            results = self.execute_query(query, fetchall=True)
            return results
        except Exception as e:
            print(f"--> Error fetching sales: {e}")
            return None

    def fetch_sales_by_date_range(self, start_date, end_date):
        query = "SELECT * FROM sales WHERE date BETWEEN %s AND %s"
        params = (start_date, end_date)
        try:
            results = self.execute_query(query, params, fetchall=True)
            return results
        except Exception as e:
            print(f"--> Error fetching sales by date range: {e}")
            return None

    # Fetch a sale by ID
    def fetch_sale_by_id(self, sale_id):
        query = "SELECT * FROM sales WHERE id=%s"
        params = (sale_id,)
        try:
            result = self.execute_query(query, params, fetchone=True)
            return result
        except Exception as e:
            print(f"--> Error fetching sale by ID: {e}")
            return None
    
    # search sales by cashier name
    def search_sales_by_cashier_name(self, cashier_name):
        query = "SELECT * FROM sales WHERE cashier_name LIKE %s"
        params = (f"%{cashier_name}%",)
        try:
            results = self.execute_query(query, params, fetchall=True)
            return results
        except Exception as e:
            print(f"--> Error searching sales by cashier name: {e}")
            return None

    # Update a sale
    def update_sale(self, sale_id, total_amount=None, cashier_id=None, cashier_name=None, payment_method=None):
        query = "UPDATE sales SET "
        params = []

        if total_amount:
            query += "total_amount=%s, "
            params.append(total_amount)
        if cashier_id:
            query += "cashier_id=%s, "
            params.append(cashier_id)
        if payment_method:
            query += "payment_method=%s, "
            params.append(payment_method)
        if cashier_name:
            query += "cashier_name=%s "
            params.append(cashier_name)

        query = query.rstrip(", ") + " WHERE id=%s"
        params.append(sale_id)
        try:
            self.execute_query(query, params)
            print(f"--> Sale: ({sale_id}) has been updated successfully!")
        except Exception as e:
            print(f"--> Error updating sale: {e}")
            raise Exception(f"Error updating sale{sale_id}: {e}")

    # Delete a sale
    def delete_sale(self, sale_id):
        query = "DELETE FROM sales WHERE id=%s"
        params = (sale_id,)
        try:
            self.execute_query(query, params)
            print(f"--> Sale: ({sale_id}) has been deleted successfully!")
        except Exception as e:
            print(f"--> Error deleting sale: {e}")
            raise Exception

    # Clear all sales
    def clear_all_sales(self):
        query = "DELETE FROM sales"
        try:
            self.execute_query(query)
            print("--> All sales have been cleared successfully!")
        except Exception as e:
            print(f"--> Error clearing sales: {e}")






    #! Add a sale item --------------------------------------------------------------
    def add_sale_item(self, sale_id, product_id, quantity, unit_price, subtotal):
        query = "INSERT INTO sales_items(sale_id, product_id, quantity, unit_price, subtotal) VALUES(%s, %s, %s, %s, %s)"
        params = (sale_id, product_id, quantity, unit_price, subtotal)
        try:
            self.execute_query(query, params)
            print(f"--> Sale Item: ({product_id}) has been added into the database successfully!")
        except Exception as e:
            print(f"--> Error inserting sale item: {e}")

    # Fetch all sale items
    def fetch_all_sale_items(self):
        query = "SELECT * FROM sales_items"
        try:
            results = self.execute_query(query, fetchall=True)
            return results
        except Exception as e:
            print(f"--> Error fetching sale items: {e}")
            return None
    
    # Fetch a sale item by ID
    def fetch_sale_item_by_id(self, sale_item_id):
        query = "SELECT * FROM sales_items WHERE id=%s"
        params = (sale_item_id,)
        try:
            result = self.execute_query(query, params, fetchone=True)
            return result
        except Exception as e:
            print(f"--> Error fetching sale item by ID: {e}")
            return None

    # Fetch sale items by sale ID
    def get_sale_items_data(self, sale_id):
        query = "SELECT * FROM sales_items WHERE sale_id=%s"
        params = (sale_id,)
        try:
            results = self.execute_query(query, params, fetchall=True)
            return results
        except Exception as e:
            print(f"--> Error fetching sale items by sale ID: {e}")
            return None

    # Update a sale item
    def update_sale_item(self, sale_item_id, sale_id=None, product_id=None, quantity=None, unit_price=None, subtotal=None):
        query = "UPDATE sales_items SET "
        params = []

        if sale_id:
            query += "sale_id=%s, "
            params.append(sale_id)
        if product_id:
            query += "product_id=%s, "
            params.append(product_id)
        if quantity:
            query += "quantity=%s, "
            params.append(quantity)
        if unit_price:
            query += "unit_price=%s, "
            params.append(unit_price)
        if subtotal:
            query += "subtotal=%s "
            params.append(subtotal)

        query = query.rstrip(", ") + " WHERE id=%s"
        params.append(sale_item_id)

        try:
            self.execute_query(query, params)
            print(f"--> Sale Item: ({sale_item_id}) has been updated successfully!")
        except Exception as e:
            print(f"--> Error updating sale item: {e}")

    # Delete a sale item
    def delete_sale_item(self, sale_item_id):
        query = "DELETE FROM sales_items WHERE id=%s"
        params = (sale_item_id,)
        try:
            self.execute_query(query, params)
            print(f"--> Sale Item: ({sale_item_id}) has been deleted successfully!")
        except Exception as e:
            print(f"--> Error deleting sale item: {e}")

    # Clear all sale items
    def clear_all_sale_items(self):
        query = "DELETE FROM sales_items"
        try:
            self.execute_query(query)
            print("--> All sale items have been cleared successfully!")
        except Exception as e:
            print(f"--> Error clearing sale items: {e}")

    # Close the database connection
    def close_connection(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        print("Database connection closed successfully!")

if __name__ == "__main__":
    db = Database(host="127.0.0.1", username="root", password="Tokata@se7en232722", database="POS_DB")

    # Initialize all tables if they don't exist yet
    db.initialize_tables()


