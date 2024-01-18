import streamlit as st
import sqlite3
from datetime import datetime,timedelta

class ModifyInventory:
    def __init__(self):
        pass

    def add_or_modify_item(self, sku_id, item_name, buy_price, sell_price, quantity):
        conn = sqlite3.connect("inventory.db")
        cursor = conn.cursor()

        try:
            current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Check if SKU ID already exists
            cursor.execute("SELECT COUNT(*) FROM items WHERE sku_id=?", (sku_id,))
            count = cursor.fetchone()[0]

            if count > 0:
                # SKU ID exists, update the item
                cursor.execute("""
                    UPDATE items
                    SET item_name=?, sell_price=?, buy_price=?, quantity=?, added_datetime=?
                    WHERE sku_id=?
                """, (item_name, sell_price, buy_price, quantity, current_datetime, sku_id))
                st.success(f"Item {sku_id} modified successfully at {current_datetime}!")
            else:
                # SKU ID doesn't exist, add a new item
                cursor.execute("""
                    INSERT INTO items VALUES (?, ?, ?, ?, ?, ?)
                """, (sku_id, item_name, sell_price, buy_price, quantity, current_datetime))
                st.success(f"Item {sku_id} added successfully at {current_datetime}!")

            conn.commit()
        except sqlite3.IntegrityError:
            st.warning(f"Item {sku_id} already exists in the database. Use a different SKU ID.")
        finally:
            conn.close()

    def remove_item(self, sku_id):
        conn = sqlite3.connect("inventory.db")
        cursor = conn.cursor()

        try:
            # Check if SKU ID exists
            cursor.execute("SELECT COUNT(*) FROM items WHERE sku_id=?", (sku_id,))
            count = cursor.fetchone()[0]

            if count > 0:
                # SKU ID exists, remove the item
                cursor.execute("DELETE FROM items WHERE sku_id=?", (sku_id,))
                st.success(f"Item {sku_id} removed successfully!")
            else:
                st.warning(f"Item with SKU ID {sku_id} not found in the inventory.")

            conn.commit()
        finally:
            conn.close()

    def run_web_app(self):
        st.title("Inventory Management System - Modify Inventory")
        barcode_icon_path = "barcode.png"  # Replace with the actual path to your barcode icon image
        st.image(barcode_icon_path, width=150)
        scan_with_barcode = st.checkbox("Scan with Barcode")
        # Display additional content if the toggle is activated
        if scan_with_barcode:
            st.write("Barcode scanning is enabled. Ready to scan...")
        else:
            st.write("Barcode scanning is disabled.")
        # User input for item details
        sku_id = st.text_input("Enter SKU ID:")
        item_name = st.text_input("Enter Item Name:")
        buy_price = st.number_input("Enter Cost Price:", min_value=0.01)
        sell_price = st.number_input("Enter Sell Price:", min_value=0.01)
        quantity = st.number_input("Enter Quantity:", min_value=0, step=1, format="%d")

        if st.button("Add/Modify Item"):
            self.add_or_modify_item(sku_id, item_name, buy_price, sell_price, quantity)

        # Display existing items and buttons to remove them
        st.title("Existing Items in Inventory")
        st.divider()
        conn = sqlite3.connect("inventory.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM items")
        items = cursor.fetchall()
        conn.close()

        for item in items:
            self.display_existing_item(item)
            st.divider()

    def display_existing_item(self, item):
        sku_id, item_name, sell_price, buy_price, quantity, added_datetime = item

        # Display existing item details
        st.write(f"**Item Name:** {item_name}")
        st.write(f"SKU ID: {sku_id}")
        st.write(f"Buy Price: ₹{buy_price:.2f}")
        st.write(f"Sell Price: ₹{sell_price:.2f}")
        st.write(f"Quantity: {quantity}")
        st.write(f"Added Datetime: {added_datetime}")

        # Add a button to remove the item
        if st.button(f"Remove Item {sku_id}"):
            self.remove_item(sku_id)
