import os
import sqlite3

import view.register_page as register_page
import view.start_login_page as start_login_page

def initializeDb():
    conn = sqlite3.connect('database.sqlite')
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS program_info (opened_before INTEGER)')
    c.execute('CREATE TABLE IF NOT EXISTS accounts (username TEXT, password TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS tables (name TEXT, type TEXT, open_close INTEGER, feePerMinute REAL, image_path REAL)')
    c.execute('CREATE TABLE IF NOT EXISTS cafe_items (name TEXT, type TEXT, cost REAL, description TEXT, image_path TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS fees (table_id INTEGER, price REAL, duration INTEGER)')
    c.execute('INSERT INTO program_info VALUES (?)', (1,))
    conn.commit()
    conn.close()

def check_if_opened_before():
    try:
        if not os.path.exists('database.sqlite'):
            return False
        conn = sqlite3.connect('database.sqlite')
        c = conn.cursor()
        c.execute('SELECT opened_before FROM program_info')
        opened_before = c.fetchone()[0]
        conn.commit()
        conn.close()
        print(opened_before)
        return opened_before
    except Exception as e:
        print(e)
        return False


if __name__ == "__main__":
    if check_if_opened_before():
        print("Program opened before!")
        start_login_page.startLoginPage() # start your start_login_page.py

    else:
        print("First time opening the program!")
        initializeDb()
        register_page.clickCreateAccount() # start your register_page.py