from ttkthemes import ThemedTk
import view.main_page as main_page  # import main_page.py
from model.account import Account  # import account.py

def register(name_entry, password_entry,app):
    username = name_entry.get()
    password = password_entry.get()

    account = Account(username, password)
    if account.check_if_account_exists():
        print("Account already exists!")
    else:
        account.save_to_db()
        open_main_page(app)
        print("Account created successfully!")


def open_main_page(app: ThemedTk):
    app.destroy()  # close the login window
    main_page.mainPage()  # start your main_page.py
