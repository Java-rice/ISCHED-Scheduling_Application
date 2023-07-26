import sqlite3

def createdatabase():
    
    conn = sqlite3.connect(r"database.db")
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users(
            username TEXT NOT NULL,
            password TEXT NOT NULL
    )''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks(
            task_id INTEGER NOT NULL,
            username TEXT NOT NULL,
            taskname TEXT NOT NULL,
            duration INTEGER,
            duedate TEXT NOT NULL,
            duetime TEXT NOT NULL,
            importance INTEGER,
            status TEXT NOT NULL,
            PRIMARY KEY("task_id" AUTOINCREMENT)
    )''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS idletime(
            idleID INTEGER NOT NULL,
            username TEXT NOT NULL,
            starttime TEXT NOT NULL,
            endtime TEXT NOT NULL,
            date TEXT NOT NULL,
            PRIMARY KEY("idleID" AUTOINCREMENT)
    )''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS history(
            username TEXT NOT NULL,
            task_id INTEGER NOT NULL,
            task_name TEXT NOT NULL,
            currenttime TEXT NOT NULL,
            currentdate INTEGER,
            status TEXT NOT NULL
    )''')
    conn.close()