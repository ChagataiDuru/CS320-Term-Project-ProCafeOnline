from ttkthemes import ThemedTk

import view.main_page as main_page  # import main_page.py
import view.register_page as register_page  # import register_page.py

from model.account import Account  # import account.py

def login(name_entry, password_entry,app):
    username = name_entry.get()
    password = password_entry.get()

    account = Account(username, password)
    if account.check_password():
        print("Login completed successfully!")
        open_main_page(app)
    else:
        print("Invalid username or password.")

def open_register_page(app: ThemedTk):
    app.destroy()  # close the login window
    register_page.clickCreateAccount()  # start your register_page.py

def open_main_page(app: ThemedTk):
    app.destroy()  # close the login window
    main_page.mainPage()  # start your main_page.py