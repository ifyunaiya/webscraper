import sqlite3
from pages import scraper

def initialize_database(db_name = 'product_urls.db'):
    try:
        conn = sqlite3.connect(db_name)
        data = [("Hello world")]
        cursor = conn.cursor()
        cursor.execute('''
                CREATE TABLE IF NOT EXISTS product_urls( id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                            url TEXT )
        ''')
        cursor.execute('''
                INSERT INTO product_urls(url) VALUES (?)
        ''',data)
        cursor.execute('''
                SELECT name FROM sqlite_master WHERE type = 'table'
        ''')
        for row in conn.execute("SELECT * from product_urls "):
            print(row)
        
        conn.commit()

    except sqlite3.Error as error:
        print("Failed to execute the above query", error)

    finally:
        if conn:
            conn.close()
            print("The sqlite connection is now closed")
            print(scraper.df)
    
initialize_database()
                   