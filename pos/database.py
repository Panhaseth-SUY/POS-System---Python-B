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
    def execute_query(self, query, params=None, fetch=False, fetchone=False):
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
            if fetch:
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
            """CREATE TABLE IF NOT EXISTS users(
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            username VARCHAR(255) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
            role ENUM('admin', 'cashier') NOT NULL DEFAULT 'cashier'
            )""",

            """CREATE TABLE IF NOT EXISTS products(
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            price DECIMAL(10, 2) NOT NULL
            )"""
        ]
        try:
            for query in queries:
                self.execute_query(query)
            print("--> All Tables are initialized successfully!")
        except Exception as e:
            print(f"--> Error initializing tables: {e}")

    # Insert a user
    def insert_user(self, name, username, password, role):
        query = "INSERT INTO users(name, username, password, role) VALUES(%s, %s, %s, %s)"
        params = (name, username, password, role)
        try:
            self.execute_query(query, params)
            print(f"-->{name} ({role}) has been inserted into the database successfully!")
        except Exception as e:
            print(f"--> Error inserting user: {e}")

    # Fetch all users
    def fetch_all_users(self):
        query = "SELECT * FROM users"
        try:
            results = self.execute_query(query, fetch=True)
            return results
        except Exception as e:
            print(f"--> Error fetching users: {e}")
            return None

            


if __name__ == "__main__":
    db = Database()
    db.initialize_tables()
    db.insert_user("Panhaseth SUY", "admin", "admin", "admin")
    db.insert_user("Panhaseth SUY", "cashier", "cashier", "cashier")
