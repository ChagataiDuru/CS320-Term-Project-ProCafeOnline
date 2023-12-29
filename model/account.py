import sqlite3

class Account:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def save_to_db(self):
        conn = sqlite3.connect('database.sqlite')
        c = conn.cursor()
        c.execute('INSERT INTO accounts VALUES (?, ?)', (self.username, self.password))
        conn.commit()
        conn.close()

    def check_if_account_exists(self):
        conn = sqlite3.connect('database.sqlite')
        c = conn.cursor()
        c.execute('SELECT * FROM accounts WHERE username = ?', (self.username,))
        if c.fetchone() is None:
            return False
        else:
            return True
        
    def check_password(self):
        conn = sqlite3.connect('database.sqlite')
        c = conn.cursor()
        if self.check_if_account_exists():
            c.execute('SELECT * FROM accounts WHERE username = ?', (self.username,))
            result = c.fetchone()
            if result[1] == self.password:
                return True
            else:
                return False
        else:
            return False