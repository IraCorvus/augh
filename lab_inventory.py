import sqlite3
from datetime import datetime

def setup_database():
    conn = sqlite3.connect("lab_inventory.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS inventory (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        cas_number TEXT,
                        supplier TEXT,
                        quantity INTEGER,
                        storage_location TEXT,
                        expiration_date TEXT,
                        compatibility_group TEXT
                    )''')
    conn.commit()
    return conn

class InventoryManager:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()

    def add_item(self, name, cas_number, supplier, quantity, storage_location, expiration_date, compatibility_group):
        expiration_date = datetime.strptime(expiration_date, "%Y-%m-%d")
        self.cursor.execute('''INSERT INTO inventory 
                               (name, cas_number, supplier, quantity, storage_location, expiration_date, compatibility_group) 
                               VALUES (?, ?, ?, ?, ?, ?, ?)''',
                            (name, cas_number, supplier, quantity, storage_location, expiration_date, compatibility_group))
        self.conn.commit()
        print("Item added successfully.")

    def view_inventory(self):
        self.cursor.execute("SELECT * FROM inventory")
        items = self.cursor.fetchall()
        for item in items:
            print(item)

    def update_item_quantity(self, item_id, quantity):
        self.cursor.execute("UPDATE inventory SET quantity = ? WHERE id = ?", (quantity, item_id))
        self.conn.commit()
        print("Item quantity updated successfully.")

    def delete_item(self, item_id):
        self.cursor.execute("DELETE FROM inventory WHERE id = ?", (item_id,))
        self.conn.commit()
        print("Item deleted successfully.")

    def check_expiration(self):
        today = datetime.now()
        self.cursor.execute("SELECT * FROM inventory WHERE expiration_date < ?", (today.strftime("%Y-%m-%d"),))
        expired_items = self.cursor.fetchall()
        if expired_items:
            print("Expired items:")
            for item in expired_items:
                print(item)
        else:
            print("No expired items found.")

    def check_compatibility(self, new_item_group, storage_location):
        self.cursor.execute("SELECT * FROM inventory WHERE storage_location = ?", (storage_location,))
        items_in_location = self.cursor.fetchall()
        incompatible = [item for item in items_in_location if item[7] != new_item_group]
        if incompatible:
            print("Warning: Incompatible items found in storage location!")
            for item in incompatible:
                print(item)
        else:
            print("All items in this storage location are compatible.")

def main():
    conn = setup_database()
    inventory = InventoryManager(conn)
    
    print("Welcome to Lab Inventory Manager")
    while True:
        print("\nOptions: add, view, update, delete, check_expiration, check_compatibility, exit")
        action = input("Choose an action: ").strip().lower()
        
        if action == "add":
            name = input("Item name: ")
            cas_number = input("CAS number: ")
            supplier = input("Supplier: ")
            quantity = int(input("Quantity: "))
            storage_location = input("Storage location: ")
            expiration_date = input("Expiration date (YYYY-MM-DD): ")
            compatibility_group = input("Compatibility group: ")
            inventory.add_item(name, cas_number, supplier, quantity, storage_location, expiration_date, compatibility_group)

        elif action == "view":
            inventory.view_inventory()

        elif action == "update":
            item_id = int(input("Item ID to update: "))
            quantity = int(input("New quantity: "))
            inventory.update_item_quantity(item_id, quantity)

        elif action == "delete":
            item_id = int(input("Item ID to delete: "))
            inventory.delete_item(item_id)

        elif action == "check_expiration":
            inventory.check_expiration()

        elif action == "check_compatibility":
            new_item_group = input("Enter new item compatibility group: ")
            storage_location = input("Enter storage location: ")
            inventory.check_compatibility(new_item_group, storage_location)

        elif action == "exit":
            print("Exiting program.")
            conn.close()
            break

        else:
            print("Invalid option, please try again.")

if __name__ == "__main__":
    main()