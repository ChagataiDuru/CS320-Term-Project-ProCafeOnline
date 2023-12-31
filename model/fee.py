import sqlite3

class Fee:
    def __init__(self, table_id, price, duration):
        self.table_id = table_id
        self.price = price
        self.duration = duration

    def save_to_db(self):
        conn = sqlite3.connect('database.sqlite')
        c = conn.cursor()
        c.execute('INSERT INTO fees VALUES (?, ?, ?)', (self.table_id, self.price, self.duration))
        conn.commit()
        conn.close()