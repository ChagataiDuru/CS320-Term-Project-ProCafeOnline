import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk

from controller.start_login_page_controller import *

def startLoginPage():
    app = ThemedTk(theme="equilux")
    app.title("Login Page")
    app.geometry("1280x720")
    app.resizable(width=False, height=False)

    style = ttk.Style(app)
    style.configure('TLabel', foreground='white', font=("Roboto", 14))
    style.configure('TEntry', font=("Roboto", 14))
    style.configure('TButton', foreground='white', font=("Roboto", 14))

    background_image = tk.PhotoImage(file="assets/pcobackground.png")  
    background_label = tk.Label(app, image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    main_frame = ttk.Frame(app, width=410, height=385)
    main_frame.place(relx=0.5, rely=0.5, anchor="center")

    logo_image = tk.PhotoImage(file="assets/pco_logo.png")  
    logo_label = ttk.Label(main_frame, image=logo_image)
    logo_label.place(x=0, y=10, width=410, height=150)

    name_label = ttk.Label(main_frame, text="Name")
    name_label.place(relx=0.5, rely=0.50, anchor="center")
    name_entry = ttk.Entry(main_frame)
    name_entry.place(relx=0.5, rely=0.58, anchor="center", width=200, height=35)

    password_label = ttk.Label(main_frame, text="Password")
    password_label.place(relx=0.5, rely=0.68, anchor="center")
    password_entry = ttk.Entry(main_frame)
    password_entry.place(relx=0.5, rely=0.77, anchor="center", width=200, height=35)

    login_button = ttk.Button(main_frame, text="Login", command=lambda: login(name_entry, password_entry,app))
    login_button.place(relx=0.5, rely=0.90, anchor="center", width=200, height=35)

    register_button = ttk.Button(main_frame, text="Register new", command=lambda: open_register_page(app))
    register_button.place(relx=0.5, rely=0.98, anchor="center", width=200, height=35)

    app.mainloop()


