import mysql.connector

class Database:
    def __init__(self, host="127.0.0.1", username="root", password="Tokata@se7en232722", database="POS_DB"):
        self.host = host
        self.username = username
        self.password = password
        self.database = database

    # Connect to the database (return connection)
    def connect_db(self):
        try:
            conn = mysql.connector.connect(
                host=self.host,
                user=self.username,
                password=self.password,
                database=self.database
            )
            if conn.is_connected():
                return conn
        except mysql.connector.Error as e:
            raise Exception(f"Database connection failed: {e}")

    # Execute a query (return result if fetch=True, fetchone=True, or None)
    def execute_query(self, query, params=None, fetchall=False, fetchone=False):
        conn = None
        cursor = None
        try:
            conn = self.connect_db()
            cursor = conn.cursor(dictionary=True)
            
            # Execute query with or without parameters
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            # Handle fetching data for SELECT queries
            if fetchall:
                return cursor.fetchall()
            elif fetchone:
                return cursor.fetchone()
            
            # Commit changes for non-SELECT queries
            conn.commit()
        except mysql.connector.Error as e:
            raise Exception(f"Query execution failed: {e}")
        finally:
            # Ensure cursor and connection are always closed
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    # Initialize all tables for database
    def initialize_tables(self):
        queries = [
            """CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            username VARCHAR(50) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL, 
            role ENUM('Admin', 'Cashier', 'Manager') NOT NULL DEFAULT 'Cashier',
            status ENUM('Active', 'Inactive') NOT NULL DEFAULT 'Active', -- User account status
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )""",

            """CREATE TABLE IF NOT EXISTS categories (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL UNIQUE,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )""",

            """CREATE TABLE IF NOT EXISTS products (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            sku VARCHAR(50) NOT NULL UNIQUE,
            barcode VARCHAR(50) NOT NULL UNIQUE,
            description TEXT,
            price DECIMAL(10, 2) NOT NULL,
            stock_quantity INT NOT NULL,
            category_id INT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (category_id) REFERENCES categories(id)
            )""",

            """CREATE TABLE IF NOT EXISTS sales (
            id INT AUTO_INCREMENT PRIMARY KEY,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            total_amount DECIMAL(10, 2) NOT NULL,
            cashier_id INT,
            payment_method ENUM('Cash', 'Card', 'Digital Wallet') NOT NULL,
            status ENUM('Completed', 'Pending', 'Canceled') DEFAULT 'Completed',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (cashier_id) REFERENCES users(id)
            )""",

            """CREATE TABLE IF NOT EXISTS sales_items (
            id INT AUTO_INCREMENT PRIMARY KEY,
            sale_id INT,
            product_id INT,
            quantity INT NOT NULL,
            unit_price DECIMAL(10, 2) NOT NULL,
            subtotal DECIMAL(10, 2) NOT NULL, -- quantity * unit_price
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (sale_id) REFERENCES sales(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
            )""",

            """CREATE TABLE IF NOT EXISTS inventory_logs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            product_id INT,
            change_quantity INT NOT NULL,
            reason VARCHAR(255), -- e.g., "Restock", "Sale", "Adjustment"
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products(id)
            )"""
        ]
        try:
            for query in queries:
                self.execute_query(query)
            print("--> All Tables are initialized successfully!")
        except Exception as e:
            print(f"--> Error initializing tables: {e}")

    # Add a user
    def add_user(self, name, username, password, role):
        query = "INSERT INTO users(name, username, password, role) VALUES(%s, %s, %s, %s)"
        params = (name, username, password, role)
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
    def update_user(self, username, name, password, role):
        query = "UPDATE users SET name=%s, password=%s, role=%s WHERE username=%s"
        params = (name, password, role, username)
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

    # Authenticate
    def authenticate_user(self, username, password):
        query = "SELECT * FROM users WHERE username=%s AND password=%s"
        params = (username, password)
        try:
            result = self.execute_query(query, params, fetchone=True)
            return result
        except Exception as e:
            print(f"--> Error authenticating user: {e}")
            return False
            
    # Add a product
    def add_product(self, name, sku, barcode, description, price, stock_quantity, category_id):
        query = "INSERT INTO products(name, sku, barcode, description, price, stock_quantity, category_id) VALUES(%s, %s, %s, %s, %s, %s, %s)"
        params = (name, sku, barcode, description, price, stock_quantity, category_id)
        try:
            self.execute_query(query, params)
            print(f"-->Product: ({name}) has been added into the database successfully!")
        except Exception as e:
            print(f"--> Error inserting product: {e}")

    # Fetch all products
    def fetch_all_products(self):
        query = "SELECT * FROM products"
        try:
            results = self.execute_query(query, fetchall=True)
            return results
        except Exception as e:
            print(f"--> Error fetching products: {e}")
            return None
    
    # Fetch a product by ID
    def fetch_product_by_id(self, product_id):
        query = "SELECT * FROM products WHERE id=%s"
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

    # Add a category
    def add_category(self, name, description=None):
        query = "INSERT INTO categories(name, description) VALUES(%s, %s)"
        params = (name, description)
        try:
            self.execute_query(query, params)
            print(f"-->Category: ({name}) has been added into the database successfully!")
        except Exception as e:
            print(f"--> Error inserting category: {e}")

    # Fetch all categories
    def fetch_all_categories(self):
        query = "SELECT * FROM categories"
        try:
            results = self.execute_query(query, fetchall=True)
            return results
        except Exception as e:
            print(f"--> Error fetching categories: {e}")
            return None
        
    # Fetch a category by ID
    def fetch_category_by_id(self, category_id):
        query = "SELECT * FROM categories WHERE id=%s"
        params = (category_id,)
        try:
            result = self.execute_query(query, params, fetchone=True)
            return result
        except Exception as e:
            print(f"--> Error fetching category by ID: {e}")
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

    # Add a sale
    def add_sale(self, total_amount, cashier_id, payment_method):
        query = "INSERT INTO sales(total_amount, cashier_id, payment_method) VALUES(%s, %s, %s)"
        params = (total_amount, cashier_id, payment_method)
        try:
            self.execute_query(query, params)
            print(f"-->Sale by cashier({cashier_id}) has been added into the database successfully!")
        except Exception as e:
            print(f"--> Error inserting sale: {e}")

    # Fetch all sales
    def fetch_all_sales(self):
        query = "SELECT * FROM sales"
        try:
            results = self.execute_query(query, fetchall=True)
            return results
        except Exception as e:
            print(f"--> Error fetching sales: {e}")
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
        
    # Update a sale
    def update_sale(self, sale_id, total_amount=None, cashier_id=None, payment_method=None):
        query = "UPDATE sales SET "
        params = []

        if total_amount:
            query += "total_amount=%s, "
            params.append(total_amount)
        if cashier_id:
            query += "cashier_id=%s, "
            params.append(cashier_id)
        if payment_method:
            query += "payment_method=%s "
            params.append(payment_method)

        query = query.rstrip(", ") + " WHERE id=%s"
        params.append(sale_id)
        try:
            self.execute_query(query, params)
            print(f"--> Sale: ({sale_id}) has been updated successfully!")
        except Exception as e:
            print(f"--> Error updating sale: {e}")

    # Delete a sale
    def delete_sale(self, sale_id):
        query = "DELETE FROM sales WHERE id=%s"
        params = (sale_id,)
        try:
            self.execute_query(query, params)
            print(f"--> Sale: ({sale_id}) has been deleted successfully!")
        except Exception as e:
            print(f"--> Error deleting sale: {e}")

    # Add a sale item
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

    # Add an inventory log
    def add_inventory_log(self, product_id, change_quantity, reason):
        query = "INSERT INTO inventory_logs(product_id, change_quantity, reason) VALUES(%s, %s, %s)"
        params = (product_id, change_quantity, reason)
        try:
            self.execute_query(query, params)
            print(f"--> Inventory Log: ({product_id}) has been added into the database successfully!")
        except Exception as e:
            print(f"--> Error inserting inventory log: {e}")

    # Fetch all inventory logs
    def fetch_all_inventory_logs(self):
        query = "SELECT * FROM inventory_logs"
        try:
            results = self.execute_query(query, fetchall=True)
            return results
        except Exception as e:
            print(f"--> Error fetching inventory logs: {e}")
            return None
        
    # Fetch an inventory log by ID
    def fetch_inventory_log_by_id(self, inventory_log_id):
        query = "SELECT * FROM inventory_logs WHERE id=%s"
        params = (inventory_log_id,)
        try:
            result = self.execute_query(query, params, fetchone=True)
            return result
        except Exception as e:
            print(f"--> Error fetching inventory log by ID: {e}")
            return None
        
    # Update an inventory log
    def update_inventory_log(self, inventory_log_id, product_id=None, change_quantity=None, reason=None):
        query = "UPDATE inventory_logs SET "
        params = []

        if product_id:
            query += "product_id=%s, "
            params.append(product_id)
        if change_quantity:
            query += "change_quantity=%s, "
            params.append(change_quantity)
        if reason:
            query += "reason=%s "
            params.append(reason)
        query = query.rstrip(", ") + " WHERE id=%s"
        params.append(inventory_log_id)
        try:
            self.execute_query(query, params)
            print(f"--> Inventory Log: ({inventory_log_id}) has been updated successfully!")
        except Exception as e:
            print(f"--> Error updating inventory log: {e}")

    # Delete an inventory log
    def delete_inventory_log(self, inventory_log_id):
        query = "DELETE FROM inventory_logs WHERE id=%s"
        params = (inventory_log_id,)
        try:
            self.execute_query(query, params)
            print(f"--> Inventory Log: ({inventory_log_id}) has been deleted successfully!")
        except Exception as e:
            print(f"--> Error deleting inventory log: {e}")

    # Close the database connection
    def close_connection(self):
        self.cursor.close()
        self.connection.close()
        print("Database connection closed successfully!")

if __name__ == "__main__":
    db = Database(host="127.0.0.1", username="root", password="Tokata@se7en232722", database="POS_DB")

    # Initialize all tables if they don't exist yet
    db.initialize_tables()


