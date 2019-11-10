#!/usr/bin/env python

from application import AllTypes
import psycopg2

if __name__ == "__main__":
    db = psycopg2.connect('')
    cursor = db.cursor()

    for t in AllTypes:
        print(t.name)
        cursor.execute(t.schema)

    db.commit()
    db.close()
