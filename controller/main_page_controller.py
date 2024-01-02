import threading
import time
import sqlite3
from datetime import datetime, timedelta

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, Tk
from PIL import Image, ImageTk, ImageOps

from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle
from reportlab.platypus import Table as ReportLabTable
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet

from model import Table, CafeItem,Fee

#----------------METHODS PART----------------


#----------------Login Methods----------------
def get_last_registered_user():
    conn = sqlite3.connect('database.sqlite')
    c = conn.cursor()
    c.execute('SELECT username FROM accounts ORDER BY rowid DESC LIMIT 1')
    last_registered_user = c.fetchone()
    conn.commit()
    conn.close()
    return last_registered_user[0] if last_registered_user else None

#----------------Table Methods--------------------
def upload_image(label):
    root = Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", ".png .jpg .jpeg .gif")])
    root.destroy()  # Destroy the root window

    if file_path:
        label.config(text=file_path)

def save_table(name, type, fee, image_path, window, table_tree):
    try:
        fee = int(fee)
        new_table = Table(name, type, False, fee, 0, 0, 0, image_path, 0)
        new_table.save_to_db()
        tables.append(new_table)
        print("TABLES",tables)
        update_treeview(table_tree)
        window.destroy()
    except ValueError:
        messagebox.showerror("Error", "Invalid input in one or more fields")


# A dictionary to hold the references to the images
image_refs = {}
def update_treeview(table_tree: ttk.Treeview):
    global image_refs
    image_refs.clear()  # Clear existing image references

    for i in table_tree.get_children():
        table_tree.delete(i)

    for table in tables:
        print("TABLE",table)
        open_close_status = "Open" if table.open_close else "Closed"
        if table.image_path:
            img = Image.open(table.image_path)
            img = img.convert("RGBA")  # Ensure image is in RGBA format

            # Resize while preserving transparency
            img = ImageOps.fit(img, (100, 100), Image.Resampling.LANCZOS)
            
            photo = ImageTk.PhotoImage(img)
            image_refs[table.name] = photo
            table_tree.insert('', 'end', image=photo, values=(table.name, table.type, table.feePerMinute, table.duration, table.fee, open_close_status))
            print("TABLES-Image",tables)
        else:
            table_tree.insert('', 'end', values=(table.name, table.type, table.feePerMinute, table.duration, table.fee, open_close_status))
            print("TABLES-Noimage",tables)


def delete_selected_table(table_tree: ttk.Treeview):
    selected_item = table_tree.selection()
    if selected_item:
        # Get the name of the table from the selected item
        item_values = table_tree.item(selected_item, 'values')
        table_name = item_values[0]  # Assuming the first value is the name

        # Remove the selected item from the treeview
        table_tree.delete(selected_item)

        # Remove the corresponding table object from the database
        Table.delete_table(table_name)

def customize_window(table,table_tree: ttk.Treeview):
    # Create a new window
    customization_window = tk.Toplevel()
    customization_window.title("Customize Table")

    customization_window.configure(bg="#464646")

    # Type input
    ttk.Label(customization_window, text="Type").grid(row=0, column=0)
    type_entry = ttk.Entry(customization_window)
    type_entry.grid(row=0, column=1)
    type_entry.insert(0, table.type)

    # Fee input
    ttk.Label(customization_window, text="Fee per Minute").grid(row=1, column=0)
    fee_entry = ttk.Entry(customization_window)
    fee_entry.grid(row=1, column=1)
    fee_entry.insert(0, table.feePerMinute)

    # Submit button
    submit_button = ttk.Button(customization_window, text="Update", command=lambda: update_table(customization_window, table, type_entry.get(), fee_entry.get(), table_tree))
    submit_button.grid(row=2, column=1)

def open_customize_window(table_tree: ttk.Treeview):
    selected_item = table_tree.selection()
    if selected_item:
        item_values = table_tree.item(selected_item, 'values')
        table_name = item_values[0]

        # Find the selected table object
        selected_table = next((table for table in tables if table.name == table_name), None)
        if selected_table:
            customize_window(selected_table,table_tree)

def update_table(window, table, new_type, new_fee,table_tree: ttk.Treeview):
    try:
        new_fee = int(new_fee)
        table.type = new_type
        table.feePerMinute = new_fee
        new_table = Table(table.name, new_type, table.open_close, new_fee, table.image_path)
        new_table.update_db()
        update_treeview(table_tree)  # Refresh the treeview
        window.destroy()
    except ValueError:
        messagebox.showerror("Error", "Invalid fee input. Please enter a valid number.")


def toggle_open_close(table_tree: ttk.Treeview):
    selected_item = table_tree.selection()
    if selected_item:
        item_values = table_tree.item(selected_item, 'values')
        table_name = item_values[0]

        selected_table = next((table for table in tables if table.name == table_name), None)
        if selected_table:
            # Toggle the open/close status
            selected_table.open_close = not selected_table.open_close

            if selected_table.open_close:
                # If the table is now open, start the timer
                start_timer(selected_table,table_tree)
            else:
                # If the table is now closed, stop the timer and calculate the total fee
                stop_timer(selected_table)
            update_treeview(table_tree)


def start_timer(table,table_tree: ttk.Treeview):
    def timer():
        update_counter = 0
        while getattr(table, "timer_running", False):
            time.sleep(1)
            table.duration += 1
            update_counter += 1
            if update_counter >= 60:  # Every 60 seconds,
                update_treeview(table_tree)  # Update the treeview
                update_counter = 0  # Reset the counter

    table.timer_running = True
    t = threading.Thread(target=timer)
    t.start()


def stop_timer(table):
    table.timer_running = False


def reset_table(table_tree: ttk.Treeview):
    selected_item = table_tree.selection()
    if selected_item:
        item_values = table_tree.item(selected_item, 'values')
        table_name = item_values[0]

        selected_table = next((table for table in tables if table.name == table_name), None)
        if selected_table:
            selected_table.duration = 0
            selected_table.fee = 0
            selected_table.feeFromCafe = 0 
            selected_table.feeFromDuration = 0 
            update_treeview(table_tree)

def load_tables_from_db(table_tree: ttk.Treeview):
    print("Loading tables from database...")
    global tables
    tables = Table.get_all_tables()
    update_treeview(table_tree)

def print_fee(table_tree: ttk.Treeview):
    selected_item = table_tree.selection()
    if selected_item:
        item_values = table_tree.item(selected_item, 'values')
        table_name = item_values[0]

        selected_table = next((table for table in tables if table.name == table_name), None)
        if selected_table:
            feeFromDuration = selected_table.duration/3600 * selected_table.feePerMinute
            feeFromDuration = round(feeFromDuration, 2)
            selected_table.fee = feeFromDuration + selected_table.feeFromCafe
            print("Duration: ", selected_table.duration)
            print("Fee from duration: ", feeFromDuration)
            print("Fee from cafe: ", selected_table.feeFromCafe)
            print("Total fee: ", selected_table.fee)
            feemodel = Fee(selected_table.name, selected_table.fee, selected_table.duration)
            feemodel.save_to_db()


    # data which we are going to be displayed in a  tabular format
    utc_now = datetime.utcnow()
    utc_3 = utc_now + timedelta(hours=3)
    formatted_date = utc_3.strftime("%d/%m/%Y %H:%M:%S")
    tableData = [

    [formatted_date, "Fee Name", "Amount"],
        ["", "Fee from duration", feeFromDuration],
        ["", "Fee from cafe", selected_table.feeFromCafe],
        ["", "Total fee", selected_table.fee]
    ]
    # creating a Document structure with A4 size page
    invoice_name = "Invoice-" + selected_table.name + ".pdf"
    docu = SimpleDocTemplate(invoice_name, pagesize=A4)

    styles = getSampleStyleSheet()

    doc_style = styles["Heading1"]
    doc_style.alignment = 1

    title = Paragraph("TABLE INVOICE", doc_style)
    style = TableStyle([
            ("BOX", (0, 0), (-1, -1), 1, colors.black),
            ("GRID", (0, 0), (4, 4), 1, colors.chocolate),
            ("BACKGROUND", (0, 0), (3, 0), colors.skyblue),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
        ])
    table = ReportLabTable(tableData, style=style)
    docu.build([title, table])

#---------------------Cafe Item Methods-----------------------------


def load_cafeitems_from_db(cafeitems_tree: ttk.Treeview):
    print("Loading cafe items from database...")
    global cafeitems_array
    cafeitems_array = CafeItem.get_all_cafeitems()
    print("CAFEITEMS ARRAY",cafeitems_array)
    update_cafeitems_treeview(cafeitems_tree)


def save_cafeitem(name, cafeitem_type, description, cost, image_path, window, cafeitems_tree):
    try:
        cost = float(cost)
        new_cafeitem = CafeItem(name, cafeitem_type, cost, description, image_path)
        new_cafeitem.save_to_db()
        cafeitems_array.append(new_cafeitem)
        update_cafeitems_treeview(cafeitems_tree)
        window.destroy()
    except ValueError:
        messagebox.showerror("Error", "Invalid cost input. Please enter a valid number.")


def customize_cafeitem_window(cafeitem: CafeItem, cafeitems_tree: ttk.Treeview):
    customization_window = tk.Toplevel()
    customization_window.title("Customize Cafe Item")
    customization_window.configure(bg="#464646")
    # Type field
    ttk.Label(customization_window, text="Type:").grid(row=0, column=0)
    type_entry = ttk.Entry(customization_window)
    type_entry.grid(row=0, column=1)
    type_entry.insert(0, cafeitem.type)

    # Cost field
    ttk.Label(customization_window, text="Cost:").grid(row=1, column=0)
    cost_entry = ttk.Entry(customization_window)
    cost_entry.grid(row=1, column=1)
    cost_entry.insert(0, cafeitem.cost)

    # Description field
    ttk.Label(customization_window, text="Description:").grid(row=2, column=0)
    description_entry = ttk.Entry(customization_window)
    description_entry.grid(row=2, column=1)
    description_entry.insert(tk.END, cafeitem.description)

    # Submit button
    submit_button = ttk.Button(customization_window, text="Update Cafe Item", command=lambda: update_cafeitem(cafeitem, type_entry.get(), cost_entry.get(), description_entry.get(), customization_window, cafeitems_tree))
    submit_button.grid(row=3, column=1, pady=10)

def update_cafeitem(cafeitem, new_type, new_cost, new_description, window, cafeitems_tree):
    try:
        new_cost = float(new_cost)
        cafeitem.type = new_type
        cafeitem.cost = new_cost
        cafeitem.description = new_description
        CafeItem.update_cafeitem(cafeitem.name, new_type, new_cost, new_description, cafeitem.image_path)
        update_cafeitems_treeview(cafeitems_tree)
        window.destroy()
    except ValueError:
        messagebox.showerror("Error", "Invalid cost input. Please enter a valid number.")


cafeitem_image_refs = {}

def update_cafeitems_treeview(cafeitems_tree: ttk.Treeview):
    global cafeitem_image_refs
    cafeitem_image_refs.clear()  # Clear existing image references

    for i in cafeitems_tree.get_children():
        cafeitems_tree.delete(i)  # Clear the treeview

    for item in cafeitems_array:
        print("ITEM",item)
        if item.image_path:
            # Load and resize the image
            img = Image.open(item.image_path)
            img = img.resize((100, 100), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            cafeitem_image_refs[item.name] = photo  # Store reference to the image
            cafeitems_tree.insert('', 'end', image=photo, values=(item.name, item.type, item.description, item.cost))
        else:
            cafeitems_tree.insert('', 'end', values=(item.name, item.type, item.description, item.cost))

def delete_selected_cafeitem(cafeitems_tree: ttk.Treeview):
    selected_item = cafeitems_tree.selection()
    if selected_item:
        item_values = cafeitems_tree.item(selected_item, 'values')
        cafeitem_name = item_values[0]

        # Remove the selected item from the treeview
        cafeitems_tree.delete(selected_item)

        # Remove the corresponding cafe item from the 'cafeitems' list
        cafeitems = [item for item in cafeitems if item.name != cafeitem_name]
        CafeItem.delete_cafeitem(cafeitem_name)

def open_customize_cafeitem_window(cafeitems_tree: ttk.Treeview):
    selected_item = cafeitems_tree.selection()
    if selected_item:
        item_values = cafeitems_tree.item(selected_item, 'values')
        cafeitem_name = item_values[0]

        # Find the selected cafe item object
        selected_cafeitem = next((item for item in cafeitems_array if item.name == cafeitem_name), None)
        if selected_cafeitem:
            customize_cafeitem_window(selected_cafeitem, cafeitems_tree)


def add_cafeitem_to_table(cafeitems_tree: ttk.Treeview, table_tree: ttk.Treeview):
    selected_cafeitem = cafeitems_tree.selection()
    if selected_cafeitem:
        # Get selected cafe item details
        cafeitem_values = cafeitems_tree.item(selected_cafeitem, 'values')
        cafeitem_cost = float(cafeitem_values[3])  # Assuming cost is the fourth column

        # Open a new window to get the table name
        table_window = tk.Toplevel()
        table_window.title("Add to Table")
        table_window.configure(bg="#464646")

        ttk.Label(table_window, text="Table Name:").grid(row=0, column=0)
        table_name_entry = ttk.Entry(table_window)
        table_name_entry.grid(row=0, column=1)

        submit_button = ttk.Button(table_window, text="Add", command=lambda: update_table_fee(table_name_entry.get(), cafeitem_cost, table_window,table_tree))
        submit_button.grid(row=1, column=1, pady=10)

def update_table_fee(table_name, cafeitem_cost, window, table_tree):
    for table in tables:
        if table.name == table_name:
            table.feeFromCafe += cafeitem_cost
            table.fee = table.feeFromCafe + table.feeFromDuration
            print("TABLE FEE",table.fee)
            update_treeview(table_tree)  # Update the table_tree in the Table Menu tab
            break
    window.destroy()

    