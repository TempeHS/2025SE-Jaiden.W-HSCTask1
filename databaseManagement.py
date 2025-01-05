import sqlite3 as sql
import time
import random
import bcrypt

db_path = "./.databaseFiles/database.db"

def insertUser(username, hashed_password):
    con = sql.connect(db_path)
    cur = con.cursor()
    # Check if the username already exists
    cur.execute("SELECT COUNT(*) FROM secure_users_9f WHERE username = ?", (username,))
    if cur.fetchone()[0] > 0:
        con.close()
        raise Exception("Username already exists")
    cur.execute(
        "INSERT INTO secure_users_9f (username, password) VALUES (?, ?)",  
        (username, hashed_password),   # no sanitisation    
    )
    con.commit()
    con.close()

def retrieveUsers(username, password):
    # Connect to the database
    con = sql.connect(db_path)
    cur = con.cursor()
    # Use parameterized queries to prevent SQL injection
    cur.execute("SELECT * FROM secure_users_9f WHERE username = ?", (username,))
    user = cur.fetchone()
    con.close()
    if user and user[2] == password:  # Assuming the password is stored in the third column
        return True

def retrieveUserByUsername(username):
    conn = sql.connect(db_path)
    cur = conn.cursor()
    cur.execute(
        """
        SELECT * FROM secure_users_9f WHERE username = ?
        """,
        (username,)
    )
    user = cur.fetchone()
    conn.close()
    if user:
        return {
            'id': user[0],
            'username': user[1],
            'password': user[2]
        }
    return None