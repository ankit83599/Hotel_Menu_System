import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('hotel_menu.db')
cursor = conn.cursor()

# Create a table for the menu
cursor.execute('''
CREATE TABLE IF NOT EXISTS menu (
    item TEXT PRIMARY KEY,
    price INTEGER
)
''')

# Insert menu items into the database
menu = {
    'Pizza': 100,
    'Pasta': 80,
    'Burger': 70,
    'Salad': 60,
    'Coffee': 40,
    'Tea': 30,
    'Samosa': 20,
    'Sandwich': 50,
    'Juice': 45,
    'Ice Cream': 90,
}

for item, price in menu.items():
    cursor.execute('''
    INSERT OR IGNORE INTO menu (item, price) VALUES (?, ?)
    ''', (item, price))

# Commit the changes
conn.commit()

# Greet
print("WELCOME TO MAYUR HOTEL")
print("-----MENU-------")
cursor.execute('SELECT * FROM menu')
for item, price in cursor.fetchall():
    print(f"{item} : Rs {price}")

order_total = 0
ordered_items = []

while True:
    item = input("Enter the name of the item you want to order = ").capitalize()

    if item in menu:
        while True:
            try:
                quantity = int(input(f"How many {item}(s) would you like to order? "))
                if quantity > 0:
                    break
                else:
                    print("Please enter a positive number.")
            except ValueError:
                print("Invalid input! Please enter a number.")

        order_total += menu[item] * quantity
        ordered_items.extend([item] * quantity)
        print(f'{quantity} {item}(s) have been added to your order.')

        another_item = input("Do you want to add another item? (yes/no) ").lower()
        if another_item != 'yes':
            break
    else:
        print(f"Ordered item '{item}' is not available!")

# Summary of the order
if ordered_items:
    print("\n--- Order Summary ---")
    unique_items = set(ordered_items)
    for ordered_item in unique_items:
        item_quantity = ordered_items.count(ordered_item)
        print(f"{ordered_item} x{item_quantity} : Rs {menu[ordered_item]} each, Total: Rs {menu[ordered_item] * item_quantity}")
    print(f"\nThe total amount to pay is Rs {order_total}")

    # Insert order details into the orders table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item TEXT,
        quantity INTEGER,
        total_price INTEGER
    )
    ''')
    
    for ordered_item in unique_items:
        item_quantity = ordered_items.count(ordered_item)
        total_price = menu[ordered_item] * item_quantity
        cursor.execute('''
        INSERT INTO orders (item, quantity, total_price) VALUES (?, ?, ?)
        ''', (ordered_item, item_quantity, total_price))
    
    # Commit the changes
    conn.commit()

else:
    print("No items were ordered.")

# Thank the customer and exit
print("Thank you for visiting Mayur Hotel!")

# Close the database connection
conn.close()

