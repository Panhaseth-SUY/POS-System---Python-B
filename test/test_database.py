import sys
import os
# Add the project root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from pprint import pprint
from pos.database import Database

if __name__ == '__main__':
    db = Database()
### Test users table 
    # Add some users by default into the database
    # db.add_user(name="Panhaseth SUY", username="admin", password="admin-tokata", role="admin") 
    # db.add_user(name="John Wick", username="Wicky-me", password="wicky-wicky123", role="manager")
    # db.add_user(name="Alice", username="Alice", password="alice123", role="cashier")
    # db.add_user(name="Bob", username="Bob", password="bob123", role="cashier")
    # db.add_user(name="Charlie", username="Charlie", password="charlie123", role="cashier")
    # db.add_user(name="David", username="David", password="david123", role="cashier")

    # fetch all users
    # pprint(db.fetch_all_users())

    # fetch a user by username
    # pprint(db.fetch_user_by_username('admin'))

    # update a user
    # db.update_user('admin', 'TOKATA-UPDATE', 'admin', 'admin')

    # delete a user
    # db.delete_user('admin')

    # clear all users except admin
    # db.clear_all_users()

    # authenticate a user by username and password
    # pprint(db.authenticate_user('admin', 'admin-tokata'))

### Test categories table
    # Insert some categories by default into the database
    # db.add_category("Snack")
    # db.add_category("Fruit")
    # db.add_category("Vegetable")
    # db.add_category("Meat")
    # db.add_category("Fish")
    # db.add_category("Bakery")
    # db.add_category("Candy")
    # db.add_category("Ice Cream")
    # db.add_category("Beverage")
    # db.add_category("Wine")
    # db.add_category("Beer")
    # db.add_category("Whiskey")

    # Add categories from datasets
    # db.add_categories_from_dataset()

    # fetch all categories
    # pprint(db.fetch_all_categories())

    # fetch a category by id
    # pprint(db.fetch_category_by_id(1))

    # update a category
    # db.update_category(1, "Snack-UPDATE")

    # delete a category
    # db.delete_category(1)


### Test products table
    # Insert some products by default into the database
    # # (name, sku, barcode, description, price, stock_quantity, category_id)
    # db.add_product("Lays", "Lays-001", "Lays-001", "Lays Chips", 0.75, 100, 1)
    # db.add_product("Coca-Cola", "Coca-Cola-001", "Coca-Cola-001", "Coca-Cola Can", 1.00, 100, 9)
    # db.add_product("Sprite", "Sprite-001", "Sprite-001", "Sprite Can", 1.00, 100, 9)
    # db.add_product("Fanta", "Fanta-001", "Fanta-001", "Fanta Can", 1.00, 100, 9)
    # db.add_product("Pepsi", "Pepsi-001", "Pepsi-001", "Pepsi Can", 1.00, 100, 9)
    # db.add_product("Chicken Wings", "Chicken-Wings-001", "Chicken-Wings-001", "Chicken Wings", 5.00, 100, 4)
    # db.add_product("Chicken Nuggets", "Chicken-Nuggets-001", "Chicken-Nuggets-001", "Chicken Nuggets", 3.00, 100, 4)
    # db.add_product("Beef", "Beef-001", "Beef-001", "Beef", 10.00, 100, 4)
    # db.add_product("Pork", "Pork-001", "Pork-001", "Pork", 8.00, 100, 4)
    # db.add_product("Fish", "Fish-001", "Fish-001", "Fish", 6.00, 100, 5)
    # db.add_product("Salmon", "Salmon-001", "Salmon-001", "Salmon", 12.00, 100, 5)
    # db.add_product("Tuna", "Tuna-001", "Tuna-001", "Tuna", 10.00, 100, 5)
    # db.add_product("Apple", "Apple-001", "Apple-001", "Apple", 1.00, 100, 2)
    # db.add_product("Banana", "Banana-001", "Banana-001", "Banana", 0.50, 100, 2)
    # db.add_product("Orange", "Orange-001", "Orange-001", "Orange", 0.75, 100, 2)
    # db.add_product("Peach", "Peach-001", "Peach-001", "Peach", 1.00, 100, 2)
    # db.add_product("Carrot", "Carrot-001", "Carrot-001", "Carrot", 0.25, 100, 3)
    # db.add_product("Cucumber", "Cucumber-001", "Cucumber-001", "Cucumber", 0.50, 100, 3)
    # db.add_product("Tomato", "Tomato-001", "Tomato-001", "Tomato", 0.75, 100, 3)
    # db.add_product("Potato", "Potato-001", "Potato-001", "Potato", 0.50, 100, 3)
    # db.add_product("Bread", "Bread-001", "Bread-001", "Bread", 1.00, 100, 6)
    # db.add_product("Croissant", "Croissant-001", "Croissant-001", "Croissant", 1.50, 100, 6)
    # db.add_product("Donut", "Donut-001", "Donut-001", "Donut", 0.75, 100, 6)
    # db.add_product("Candy", "Candy-001", "Candy-001", "Candy", 0.25, 100, 7)
    # db.add_product("Chocolate", "Chocolate-001", "Chocolate-001", "Chocolate", 1.00, 100, 7)
    # db.add_product("Ice Cream", "Ice-Cream-001", "Ice-Cream-001", "Ice Cream", 2.00, 100, 8)
    # db.add_product("Vanilla", "Vanilla-001", "Vanilla-001", "Vanilla", 2.00, 100, 8)
    # db.add_product("Strawberry", "Strawberry-001", "Strawberry-001", "Strawberry", 2.00, 100, 8)
    # db.add_product("Red Wine", "Red-Wine-001", "Red-Wine-001", "Red Wine", 10.00, 100, 10)
    # db.add_product("White Wine", "White-Wine-001", "White-Wine-001", "White Wine", 10.00, 100, 10)
    # db.add_product("Rose Wine", "Rose-Wine-001", "Rose-Wine-001", "Rose Wine", 10.00, 100, 10)
    # db.add_product("Beer", "Beer-001", "Beer-001", "Beer", 2.00, 100, 11)
    # db.add_product("Whiskey", "Whiskey-001", "Whiskey-001", "Whiskey", 5.00, 100, 12)

    # Add products from datasets
    # db.add_products_from_dataset()

    # fetch all products
    # pprint(db.fetch_all_products())

    # Save products tables as excel files
    # db.save_products_table_as_excel_file()

    # fetch a product by id
    # pprint(db.fetch_product_by_id(1))

    # update a product
    # db.update_product(1, "Lays-UPDATE", "Lays-001", "Lays Chips", 0.75, 100, 1)

    # delete a product
    # db.delete_product(1)

    # clear all products
    # db.clear_all_products()


### Test sales table
    # Insert some sales by default into the database
    # (total_amount, cashier_id, payment_method)
    # db.add_sale(10.00, 3, "Cash")
    # db.add_sale(12.00, 3, "Card")
    # db.add_sale(40.00, 4, "Digital Wallet")
    # db.add_sale(45.00, 7, "Cash")

    # Add sales from datasets
    # db.add_sales_from_dataset()

    # fetch all sales
    # pprint(db.fetch_all_sales())

    # fecth sales from date range
    # pprint(db.fetch_sales_by_date_range("2012-11-09 00:00:00", "2013-02-26 23:59:59"))

    # fetch a sale by id
    # pprint(db.fetch_sale_by_id(9))

    # update a sale
    # db.update_sale(9, total_amount=12.00)

    # delete a sale
    # db.delete_sale(9)

    # clear all sales
    # db.clear_all_sales()

### Test sale_items table
    # Insert some sale items by default into the database
    # ( sale_id, product_id, quantity, unit_price, subtotal)
    # db.add_sale_item(4, 10, 10, 0.75, 7.50)
    # db.add_sale_item(4, 11, 10, 5.00, 50.00)
    # db.add_sale_item(4, 12, 10, 3.00, 30.00)
    # db.add_sale_item(4, 13, 10, 10.00, 100.00)
    # db.add_sale_item(4, 34, 10, 6.00, 60.00)
    # db.add_sale_item(4, 15, 10, 12.00, 120.00)
    # db.add_sale_item(4, 16, 10, 1.00, 10.00)
    # db.add_sale_item(4, 17, 10, 0.50, 5.00)
    # db.add_sale_item(5, 18, 10, 0.75, 7.50)
    # db.add_sale_item(5, 33, 10, 0.50, 5.00)
    # db.add_sale_item(5, 25, 10, 1.00, 10.00)
    # db.add_sale_item(5, 26, 10, 1.50, 15.00)
    # db.add_sale_item(5, 27, 10, 0.75, 7.50)
    # db.add_sale_item(5, 28, 10, 0.25, 2.50)
    # db.add_sale_item(5, 29, 10, 1.00, 10.00)
    # db.add_sale_item(5, 30, 10, 2.00, 20.00)
    # db.add_sale_item(5, 31, 10, 10.00, 100.00)
    # db.add_sale_item(5, 32, 10, 10.00, 100.00)
    # db.add_sale_item(6, 35, 10, 1.00, 10.00)
    # db.add_sale_item(6, 36, 10, 0.50, 5.00)
    # db.add_sale_item(6, 37, 10, 0.75, 7.50)
    # db.add_sale_item(6, 39, 10, 1.00, 10.00)
    # db.add_sale_item(6, 40, 10, 1.50, 15.00)
    # db.add_sale_item(6, 41, 10, 0.75, 7.50)

    # fetch all sale items
    # pprint(db.fetch_all_sale_items())

    # fetch a sale item by id
    # pprint(db.fetch_sale_item_by_id(1))

    # update a sale item
    # db.update_sale_item(3, quantity=20)

    # delete a sale item
    # db.delete_sale_item(3)

### Test reports (do not implement yet) ###

    # Fetch total sales for each product
    # pprint(db.fetch_total_sales_per_product())

    # Fetch top 10 most sold products
    # pprint(db.fetch_top_10_most_sold_products())

    # Fetch total sales for each category
    # pprint(db.fetch_total_sales_per_category())

    # Fetch total sales for each payment method
    # pprint(db.fetch_total_sales_per_payment_method())

    # Fetch average sales per day
    # pprint(db.fetch_average_sales_per_day())

    # Fetch average sales per week
    # pprint(db.fetch_average_sales_per_week())

    # Fetch average sales per month
    # pprint(db.fetch_average_sales_per_month())

    # Fetch average sales per year
    # pprint(db.fetch_average_sales_per_year())

    # Fetch sales per day for a specific month
    # pprint(db.fetch_sales_per_day_for_month(2))

    # Fetch sales per week for a specific month
    # pprint(db.fetch_sales_per_week_for_month(2))

    # Fetch sales per month for a specific year
    # pprint(db.fetch_sales_per_month_for_year(2022))

    # Fetch sales per year for a specific category
    # pprint(db.fetch_sales_per_year_for_category("Beer"))

    # Fetch sales per year for a specific payment method
    # pprint(db.fetch_sales_per_year_for_payment_method("Card"))















   
    

















