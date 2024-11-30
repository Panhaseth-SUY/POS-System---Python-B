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
    # db.add_user(name="Emily", username="Emily", password="emily123", role="cashier")
    # db.add_user(name="Frank", username="Frank", password="frank123", role="cashier")
    # db.add_user(name="Grace", username="Grace", password="grace123", role="cashier")
    # db.add_user(name="Henry", username="Henry", password="henry123", role="cashier")
    # db.add_user(name="Ivy", username="Ivy", password="ivy123", role="cashier")
    # db.add_user(name="Jack", username="Jack", password="jack123", role="cashier")
    # db.add_user(name="Karen", username="Karen", password="karen123", role="cashier")
    # db.add_user(name="Lisa", username="Lisa", password="lisa123", role="cashier")
    # db.add_user(name="Mary", username="Mary", password="mary123", role="cashier")


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


#! Test products table =================================================================
    # Insert some products by default into the database
    # # (name, sku, barcode, description, price, stock_quantity, category_id)
    # db.add_product("Lays", "Lays-001", "Lays-001", "Lays Chips", 0.75, 100, 1)
    # db.add_product("Coca-Cola", "Coca-Cola-001", "Coca-Cola-001", "Coca-Cola Can", 1.00, 100, 9)
    # db.add_product("Sprite", "Sprite-001", "Sprite-001", "Spri

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


#! Test sales table =================================================================
    # Insert some sales by default into the database
    # (total_amount, cashier_id, payment_method)
    # db.add_sale(10.00, 3, "Daro HEn", "Cash")
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

    # get last sale id 
    # pprint(db.get_last_sale_id())

    # update a sale
    # db.update_sale(sale_id=101, total_amount=100.00, cashier_id=4, cashier_name="Panhaseth SUY", payment_method="Cash")

    # delete a sale
    # db.delete_sale(9)

    # clear all sales
    # db.clear_all_sales()

### Test sale_items table
    # Insert some sale items by default into the database
    # ( sale_id, product_id, quantity, unit_price, subtotal)
    # db.add_sale_item(531, 2003, 10, 0.75, 7.50)
    # db.add_sale_item(531, 2004, 10, 1.00, 10.00)
    # db.add_sale_item(531, 2005, 10, 5.00, 50.00)
    # db.add_sale_item(531, 2006, 10, 3.00, 30.00)
    # db.add_sale_item(531, 2007, 10, 6.00, 60.00)
    # db.add_sale_item(531, 2008, 10, 12.00, 120.00)
    # db.add_sale_item(531, 2009, 10, 10.00, 100.00)
    # db.add_sale_item(531, 2010, 10, 1.00, 10.00)
    # db.add_sale_item(531, 2011, 10, 0.50, 5.00)
    # db.add_sale_item(531, 2012, 10, 0.75, 7.50)
    # db.add_sale_item(531, 2013, 10, 0.25, 2.50)
    # db.add_sale_item(531, 2014, 10, 0.50, 5.00)
    # db.add_sale_item(531, 2015, 10, 0.75, 7.50)
    # db.add_sale_item(531, 2016, 10, 1.00, 10.00)
    # db.add_sale_item(531, 2017, 10, 0.50, 5.00)
    # db.add_sale_item(531, 2018, 10, 0.75, 7.50)
    # db.add_sale_item(531, 2019, 10, 1.00, 10.00)
    # db.add_sale_item(531, 2020, 10, 0.50, 5.00)
    # db.add_sale_item(531, 2021, 10, 0.75, 7.50)
    # db.add_sale_item(531, 2022, 10, 1.00, 10.00)
    # db.add_sale_item(531, 2023, 10, 5.00, 50.00)
    # db.add_sale_item(531, 2024, 10, 3.00, 30.00)
    # db.add_sale_item(531, 2025, 10, 6.00, 60.00)
    # db.add_sale_item(531, 2026, 10, 12.00, 120.00)
    # db.add_sale_item(531, 2027, 10, 10.00, 100.00)
    # db.add_sale_item(531, 2028, 10, 1.00, 10.00)
    # db.add_sale_item(531, 2029, 10, 0.50, 5.00)
    # db.add_sale_item(531, 2030, 10, 0.75, 7.50)
    # db.add_sale_item(531, 2031, 10, 0.25, 2.50)
    # db.add_sale_item(531, 2032, 10, 0.50, 5.00)
    # db.add_sale_item(531, 2033, 10, 0.75, 7.50)
    # db.add_sale_item(531, 2034, 10, 1.00, 10.00)
    # db.add_sale_item(531, 2035, 10, 0.50, 5.00)
    # db.add_sale_item(531, 2036, 10, 0.75, 7.50)
    # db.add_sale_item(531, 2037, 10, 1.00, 10.00)
    # db.add_sale_item(531, 2038, 10, 0.50, 5.00)


    # fetch top category
    # pprint(db.fetch_top_categories())

    # fetch top 5 categories
    # pprint(db.fetch_top_5_most_sold_categories())

    # fetch daily sale data
    # pprint(db.fetch_daily_sales_data())





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















   
    

















