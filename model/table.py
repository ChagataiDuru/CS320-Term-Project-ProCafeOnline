import sqlite3

class Table:
    def __init__(self, name, type, open_close, feePerMinute, fee=0, feeFromDuration=0, feeFromCafe=0,image_path=None,duration=0):
        self.name = name
        self.type = type
        self.open_close = open_close
        self.feePerMinute = feePerMinute
        self.image_path = image_path
        self.fee = fee  
        self.feeFromDuration = feeFromDuration
        self.feeFromCafe = feeFromCafe
        self.duration = duration

    def __str__(self):
        return f"{self.name} - {self.type} - {'Active' if self.open_close else 'Deactive'} - Total Fee: ${self.fee}"

    def save_to_db(self):
        conn = sqlite3.connect('database.sqlite')
        c = conn.cursor()
        c.execute('INSERT INTO tables VALUES (?, ?, ?, ?, ?)', (self.name, self.type, self.open_close, self.feePerMinute, self.image_path,))
        conn.commit()
        conn.close()
    
    def update_db(self):
        conn = sqlite3.connect('database.sqlite')
        c = conn.cursor()
        c.execute('UPDATE tables SET type = ?, open_close = ?, feePerMinute = ?, image_path = ? WHERE name = ?', (self.type, self.open_close, self.feePerMinute, self.image_path, self.name,))
        conn.commit()
        conn.close()
    
    @staticmethod
    def get_all_tables():
        conn = sqlite3.connect('database.sqlite')
        c = conn.cursor()
        c.execute('SELECT * FROM tables')
        table_data = c.fetchall()
        tables = []
        for table_data in table_data:
            name, type, open_close, fee_per_minute,image_path = table_data
            table = Table(name, type, open_close, fee_per_minute, image_path = image_path)
            tables.append(table)
        print("TABLES-DB",tables)
        conn.close()
        return tables
    
    @staticmethod
    def get_table(name):
        conn = sqlite3.connect('database.sqlite')
        c = conn.cursor()
        c.execute('SELECT * FROM tables WHERE name = ?', (name,))
        table = c.fetchone()
        conn.close()
        return table
    
    @staticmethod
    def delete_table(name):
        conn = sqlite3.connect('database.sqlite')
        c = conn.cursor()
        c.execute('DELETE FROM tables WHERE name = ?', (name,))
        conn.commit()
        conn.close()

    @staticmethod
    def update_table(name, duration, type, open_close, feePerMinute, fee, feeFromDuration, feeFromCafe):
        conn = sqlite3.connect('database.sqlite')
        c = conn.cursor()
        c.execute('UPDATE tables SET duration = ?, type = ?, open_close = ?, feePerMinute = ?, fee = ?, feeFromDuration = ?, feeFromCafe = ? WHERE name = ?', (duration, type, open_close, feePerMinute, fee, feeFromDuration, feeFromCafe, name))
        conn.commit()
        conn.close()