import tkinter as tk
from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedTk

from controller.main_page_controller import *

def mainPage():
    #DESIGN PART

    # Create the main window
    app = ThemedTk(theme="equilux")
    app.title("Pro Cafe Online")
    app.geometry("1280x720")
    app.resizable(width=False, height=False)

    # Create a style
    style = ttk.Style(app)
    style.configure('TLabel', foreground='white', font=("Roboto", 14))
    style.configure('TEntry', font=("Roboto", 14))
    style.configure('TButton', foreground='white', font=("Roboto", 14))
    style.configure('TNotebook.Tab', font=("Roboto", 14), padding=[10, 10], foreground='white')
    style.configure('Treeview', font=("Roboto", 14),rowheight=120, foreground="white")

    # Create a tab control (notebook)
    tab_control = ttk.Notebook(app)

    # Create tabs
    tab1 = ttk.Frame(tab_control)
    tab2 = ttk.Frame(tab_control)
    tab3 = ttk.Frame(tab_control)

    # Add tabs to notebook
    tab_control.add(tab1, text='Main Page')
    tab_control.add(tab2, text='Tables Menu')
    tab_control.add(tab3, text='Cafe Menu')
    tab_control.pack(expand=1, fill='both')

    logo_image = tk.PhotoImage(file="assets/pco_logo_large.png")
    logo_label = ttk.Label(tab1, image=logo_image)
    logo_label.pack(pady=20)

    # Create a welcome message label
    last_registered_user = get_last_registered_user()
    welcome_message = f"Welcome {last_registered_user}!" if last_registered_user else "Welcome!"
    welcome_label = ttk.Label(tab1, text=welcome_message, style='TLabel')
    welcome_label.pack()

    style.configure("Red.TLabel", background="#373737", foreground="white", font=("Roboto", 12))

    # Updates Container
    update_frame = ttk.Frame(tab1)
    update_frame.pack(fill="both", expand=True, padx=20, pady=20)

    update_note = "Recent Update:\n\n- Improved performance\n- Bug fixes\n- Added new features"
    update_label = ttk.Label(update_frame, text=update_note, style="Red.TLabel")
    update_label.pack(fill="x", anchor="n", padx=20, pady=20)

    # TABLES MENU TAB

    # Frame for Buttons
    button_frame = ttk.Frame(tab2)
    button_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)

    # Create tables list
    def add_table():
        new_window = ThemedTk(theme="equilux")
        new_window.title("Add New Table")

        # Apply styles to new window
        style = ttk.Style(new_window)
        style.configure('TLabel', foreground='white', font=("Roboto", 14))
        style.configure('TEntry', font=("Roboto", 14))
        style.configure('TButton', foreground='white', font=("Roboto", 14))

        new_window.configure(bg="#464646")

        # Input fields
        ttk.Label(new_window, text="Name", style='TLabel').grid(row=0, column=0)
        name_entry = ttk.Entry(new_window, style='TEntry')
        name_entry.grid(row=0, column=1)

        ttk.Label(new_window, text="Type", style='TLabel').grid(row=1, column=0)
        type_entry = ttk.Entry(new_window, style='TEntry')
        type_entry.grid(row=1, column=1)

        ttk.Label(new_window, text="Fee per Minute", style='TLabel').grid(row=2, column=0)
        fee_entry = ttk.Entry(new_window, style='TEntry')
        fee_entry.grid(row=2, column=1)

        # Image Upload
        ttk.Label(new_window, text="Upload Image", style='TLabel').grid(row=3, column=0)
        image_path_label = ttk.Label(new_window, text="", style='TLabel')
        image_path_label.grid(row=3, column=1)
        image_upload_button = ttk.Button(new_window, text="Upload Image", style='TButton', command=lambda: upload_image(image_path_label))
        image_upload_button.grid(row=4, column=0, columnspan=2)

        # Submit button
        submit_button = ttk.Button(new_window, text="Add Table", style='TButton', command=lambda: save_table(name_entry.get(), type_entry.get(), fee_entry.get(), image_path_label.cget("text"), new_window, table_tree))
        submit_button.grid(row=5, column=1, pady=10)

    # Add Table Button 
    add_table_button = ttk.Button(button_frame, text="Add New Table", style='TButton', command=add_table)
    add_table_button.pack(pady=5)

    # Delete Table Button 
    delete_table_button = ttk.Button(button_frame, text="Delete Table", style='TButton', command=lambda: delete_selected_table(table_tree))
    delete_table_button.pack(pady=5)

    # Customize Table Button 
    customize_table_button = ttk.Button(button_frame, text="Customize Table", command= lambda: open_customize_window(table_tree))
    customize_table_button.pack(pady=5)

    # Open/Close Button 
    open_close_button = ttk.Button(button_frame, text="Open/Close Table", command=lambda: toggle_open_close(table_tree))
    open_close_button.pack(pady=5)

    # Reset Button 
    reset_button = ttk.Button(button_frame, text="Reset", command=lambda: reset_table(table_tree))
    reset_button.pack(pady=5)



    # Treeview for tables
    table_tree = ttk.Treeview(tab2, columns=('Name', 'Type', 'Fee per Minute', 'Duration', 'Total Fee', 'Open/Close'))
    table_tree.heading('#0', text='Image')
    table_tree.heading('Name', text='Name')
    table_tree.heading('Type', text='Type')
    table_tree.heading('Fee per Minute', text='Fee per Minute')
    table_tree.heading('Duration', text='Duration')  # New column for Duration
    table_tree.heading('Total Fee', text='Total Fee')
    table_tree.heading('Open/Close', text='Open/Close')
    table_tree.column('#0', stretch=tk.NO, width=140)
    table_tree.column('Name', stretch=tk.YES, width=100)
    table_tree.column('Type', stretch=tk.YES, width=100)
    table_tree.column('Fee per Minute', stretch=tk.YES, width=100)
    table_tree.column('Duration', stretch=tk.YES, width=100)  # Set width for Duration
    table_tree.column('Total Fee', stretch=tk.YES, width=100)
    table_tree.column('Open/Close', stretch=tk.YES, width=100)
    table_tree.pack(fill='both', expand=True)


    # CAFE MENU TAB
    # Frame for Buttons
    button_frame = ttk.Frame(tab3)
    button_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)

    # Create cafe items list
    def add_cafeitem():
        cafeitem_window = tk.Toplevel()
        cafeitem_window.title("Add New Cafe Item")
        cafeitem_window.configure(bg="#464646")

        # Name field
        ttk.Label(cafeitem_window, text="Name:").grid(row=0, column=0)
        name_entry = ttk.Entry(cafeitem_window)
        name_entry.grid(row=0, column=1)

        # Type field
        ttk.Label(cafeitem_window, text="Type:").grid(row=1, column=0)
        type_entry = ttk.Entry(cafeitem_window)
        type_entry.grid(row=1, column=1)

        # Description field
        ttk.Label(cafeitem_window, text="Description:").grid(row=2, column=0)
        description_entry = ttk.Entry(cafeitem_window)
        description_entry.grid(row=2, column=1)

        # Cost field
        ttk.Label(cafeitem_window, text="Cost:").grid(row=3, column=0)
        cost_entry = ttk.Entry(cafeitem_window)
        cost_entry.grid(row=3, column=1)

        # Image Path Label
        image_path_label = ttk.Label(cafeitem_window, text="")
        image_path_label.grid(row=4, column=1)

        # Image Upload Button
        ttk.Label(cafeitem_window, text="Upload Image:").grid(row=4, column=0)
        image_upload_button = ttk.Button(cafeitem_window, text="Upload", command=lambda: upload_image(image_path_label))
        image_upload_button.grid(row=4, column=1)

        # Submit button
        submit_button = ttk.Button(cafeitem_window, text="Add Cafe Item", command=lambda: save_cafeitem(name_entry.get(), type_entry.get(), description_entry.get(), cost_entry.get(), image_path_label.cget("text"), cafeitem_window, cafeitems_tree))
        submit_button.grid(row=5, column=1, pady=10)

    # Add Table Button 
    add_cafeitem_button = ttk.Button(button_frame, text="Add New Cafe Item", style='TButton', command=add_cafeitem)
    add_cafeitem_button.pack(pady=5)

    # Delete Table Button 
    delete_cafeitem_button = ttk.Button(button_frame, text="Delete Cafe Item", style='TButton', command=lambda: delete_selected_cafeitem(cafeitems_tree))
    delete_cafeitem_button.pack(pady=5)

    # Customize Table Button 
    customize_cafeitem_button = ttk.Button(button_frame, text="Customize Cafe Item", command=lambda: open_customize_cafeitem_window(cafeitems_tree))
    customize_cafeitem_button.pack(pady=5)

    # Add Cafe Item to Table 
    add_cafeitem_to_table_button = ttk.Button(button_frame, text="Add Cafe Item to Table", command=lambda: add_cafeitem_to_table(cafeitems_tree, table_tree))
    add_cafeitem_to_table_button.pack(pady=5)


    # Treeview for tables
    cafeitems_tree = ttk.Treeview(tab3, columns=('Name', 'Type', 'Description','Cost'))
    cafeitems_tree.heading('#0', text='Image')
    cafeitems_tree.heading('Name', text='Name')
    cafeitems_tree.heading('Type', text='Type')
    cafeitems_tree.heading('Description', text='Description')
    cafeitems_tree.heading('Cost', text='Cost')
    cafeitems_tree.column('#0', stretch=tk.NO, width=140)
    cafeitems_tree.column('Name', stretch=tk.YES, width=100)
    cafeitems_tree.column('Type', stretch=tk.YES, width=100)
    cafeitems_tree.column('Description', stretch=tk.YES, width=100)
    cafeitems_tree.column('Cost', stretch=tk.YES, width=100)
    cafeitems_tree.pack(fill='both', expand=True)

    # Load cafe items from the database
    load_cafeitems_from_db(cafeitems_tree)
    load_tables_from_db(table_tree)

    app.mainloop()
