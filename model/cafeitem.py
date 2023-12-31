import sqlite3

class CafeItem:
    def __init__(self, name, type, cost, description, image_path=None):
        self.name = name
        self.type = type
        self.cost = cost
        self.description = description
        self.image_path = image_path
        
    def __str__(self):
        return f"{self.name} - {self.type} - ${self.cost} - {self.description}"
    
    def save_to_db(self):
        conn = sqlite3.connect('database.sqlite')
        c = conn.cursor()
        c.execute('INSERT INTO cafe_items VALUES (?, ?, ?, ?, ?)', (self.name, self.type, self.cost, self.description, self.image_path))
        conn.commit()
        conn.close()