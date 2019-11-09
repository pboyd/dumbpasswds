from application import AllTypes
import sqlite3

if __name__ == "__main__":
    db = sqlite3.connect('database.db')
    cursor = db.cursor()

    for t in AllTypes:
        print(t.name)
        cursor.execute(t.schema)

    db.commit()
    db.close()
