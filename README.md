# How to Run this application
1. Go to folder: pos_system/pos
2. Find file login.py 
3. Run login.py

# Project Structure
## There is 4 folders and README.md in the project:
1. assets <!-- Data folder -->
    1. datasets <!--storing products, categories, and sales data in csv or excel for import to database -->
    2. icon     <!--storing all icons for admin page -->
    3. images
        1. images  <!-- image for login page -->
    4. invoice_pdf <!-- folder to store all pdf invoice after each sale -->
    5. logo        <!-- folder to store logo of the application -->
2. pos <!-- Source code directory -->
    1. __init__.py
    2. database.py <!-- Database class: has all method to initialize connection, fetch data, and modify data -->
    3. admin.py <!-- main backend source code, responsible all user interface as the backend code -->
    4. login.py <!-- Login page, responsible for login operations, and give the admin class a user identity -->
    5. sale_report_generator.py <!-- a class to generate sale report as pdf file -->
    6. invoice_generator.py <!-- a class to generate invoice as pdf file -->
    7. add_product_dialog.py <!-- a class backend user interface dialog, responsible for adding product -->
3. test <!-- Database Class method tester -->
    1. test_database.py
4. ui
    1. add_new_product_dialog.ui <!-- ui for for adding new product -->
    2. add_new_user_dialog.ui    <!-- ui for for adding new user -->
    3. admin.ui  <!-- main ui for whole application especially for admin -->
    4. login.ui  <!-- login ui for authentication purposes -->
5. README.md    

# Main technologies and frameworks behind the application
1. MySQL as a sql database
2. Python as backend
3. PyQt5 (QtDesigner) as User Interface
4. Reportlab handle for pdf files stuff and Data virtualization
5. Pandas is a tool for statistics tasks

# How to use the application
## Authentication system
1. Allow only for authenticated users (has as account in database)
2. Only authenticated users with active status could be accessed
3. Could contact administrator for help 
4. Successfully authentication will lead to application UI page that fit with the user role
## Application UI pages
1. for admin users (fully accessible)
    1. dashboard page
    2. category page
    3. product page
    4. pos page
    5. sales page
    6. users page
2. for manager users (could access and modify 4 pages)
    1. dashboard page
    2. category page
    3. product page
    4. sales page
3. for cashier users (there is only page for pos stuff)
    1. pos page
## Features in each page of application UI
1. dashboard page
    1. has briefly information about
        1. category page
        2. product page
        3. sales page
        4. user page
2. category page
    1. category table
    2. product table for each category
    3. buttons for category pages operations
        1. add category
        2. import excel 
        3. delete category
        4. search products
3. product page
    1. button for product pages operations
        1. add product
        2. update product
        3. import excel
        4. export excel
        5. delete product
        6. reload product
        7. search
    2. product table
4. pos page 
    1. product form to take product input and add to cart
        1. product comboBox 
        2. quantity spinBox
        3. add to cart button
        4. option (auto and manual)
    2. cart table 
        1. storing on going purchase products
        2. editing product quantity
    3. product preview table 
        1. category product filter
        2. search product
        3. add product to cart
    4. button for cart table operations
        1. clear product
        2. delete product
        3. generate pdf invoice 
5. sales page
    1. button for sales page operations
        1. filter sales by date
        2. update sales
        3. import excel
        4. generate pdf salse reports
        5. delete, reload, and search sales
    2. sales table 
5. user page
    1. button for user page operations
        1. add user
        2. update user
        3. delete, reload, and search users
## Security
1. All user passwords are hashed
2. Only authorized users are allowed
2. Database connection established properly, and cursor always be closed after each operation
3. Data in table are linked together with foreign keys

# Database Structure
## There are 5 tables for storing information
1. user table
    1. user info
    2. user status
    2. user roles
2. category table
    1. category info
    2. category status
3. product table
    1. products info
    2. sku and barcode
    3. category id reference
4. sales table
    1. sales info
    2. cashier id reference
5. sale items table
    1. sale items info
    2. product id reference
    3. sale id reference

# Installing Dependencies (For Mac User)
## Install Python and PIP
1. Install Homebrew: /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

2. Install Python: brew install python
3. Check versions: 
    python3 --version
    pip3 --version
## Set Up a Virtual Environment
1. python3 -m venv venv
2. source venv/bin/activate
## Install Dependencies
1. pip install <package_name>
2. pip install -r requirements.txt
## Manage Dependencies
1. pip freeze > requirements.txt
2. pip list
## Deactivate Virtual Environment
1. deactivate
## Check all requirement packages in the requirements.txt









