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
        
    @staticmethod
    def get_all_cafeitems():
        conn = sqlite3.connect('database.sqlite')
        c = conn.cursor()
        c.execute('SELECT * FROM cafe_items')
        cafeitems_data = c.fetchall()
        conn.close()

        cafeitems = []
        for item_data in cafeitems_data:
            name, type, cost, description, image_path = item_data
            cafeitem = CafeItem(name, type, cost, description, image_path)
            cafeitems.append(cafeitem)

        return cafeitems

    @staticmethod
    def delete_cafeitem(name):
        conn = sqlite3.connect('database.sqlite')
        c = conn.cursor()
        c.execute('DELETE FROM cafe_items WHERE name = ?', (name,))
        conn.commit()
        conn.close()
    
    @staticmethod
    def get_cafeitem(name):
        conn = sqlite3.connect('database.sqlite')
        c = conn.cursor()
        c.execute('SELECT * FROM cafe_items WHERE name = ?', (name,))
        cafeitem = c.fetchone()
        conn.close()
        return cafeitem

    @staticmethod
    def update_cafeitem(name, type, cost, description, image_path):
        conn = sqlite3.connect('database.sqlite')
        c = conn.cursor()
        c.execute('UPDATE cafe_items SET type = ?, cost = ?, description = ?, image_path = ? WHERE name = ?', (type, cost, description, image_path, name))
        conn.commit()
        conn.close()