import sqlite3

class Table:
    def __init__(self, name, type, open_close, feePerMinute, fee, feeFromDuration, feeFromCafe,image_path=None,duration=0):
        self.name = name
        self.duration = duration
        self.type = type
        self.open_close = open_close
        self.feePerMinute = feePerMinute
        self.fee = fee  
        self.image_path = image_path
        self.feeFromDuration = feeFromDuration
        self.feeFromCafe = feeFromCafe
        

    def __str__(self):
        return f"{self.name} - {self.type} - {'Active' if self.open_close else 'Deactive'} - ${self.hourly_fee}/min - Total Fee: ${self.fee}"

    def save_to_db(self):
        conn = sqlite3.connect('database.sqlite')
        c = conn.cursor()
        c.execute('INSERT INTO tables VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (self.name, self.duration, self.type, self.open_close, self.feePerMinute, self.fee, self.feeFromDuration, self.feeFromCafe))
        conn.commit()
        conn.close()
    
    def update_db(self):
        conn = sqlite3.connect('database.sqlite')
        c = conn.cursor()
        c.execute('UPDATE tables SET duration = ?, type = ?, open_close = ?, feePerMinute = ?, fee = ?, feeFromDuration = ?, feeFromCafe = ? WHERE name = ?', (self.duration, self.type, self.open_close, self.feePerMinute, self.fee, self.feeFromDuration, self.feeFromCafe, self.name))
        conn.commit()
        conn.close()