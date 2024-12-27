import sqlite3 as sql
import time
import random
import bcrypt


def insertUser(username, password, DoB):
    con = sql.connect("databaseFiles/database.db")
    cur = con.cursor()
    cur.execute(
        "INSERT INTO secure_users_9f (username,password) VALUES (?,?,?)",  
        (username, password, DoB),   #no sanitisation 
    )
    con.commit()
    con.close()


def retrieveUsers(username, password):
    con = sql.connect("C:/Users/aweso/OneDrive/Documents/GitHub/2025SE-Jaiden.W-HSCTask1/databaseFiles/database.db")
    cur = con.cursor()
    cur.execute(f"SELECT * FROM secure_users_9f WHERE username = '{username}'")
    if cur.fetchone() == None:
        con.close()
        return False
    else:
        cur.execute(f"SELECT * FROM secure_users_9f WHERE password = '{password}'")
        # Plain text log of visitor count as requested by Unsecure PWA management
        with open("visitor_log.txt", "r") as file:
            number = int(file.read().strip())
            number += 1
        with open("visitor_log.txt", "w") as file:
            file.write(str(number))
        # Simulate response time of heavy app for testing purposes
        time.sleep(random.randint(80, 90) / 1000)
        if cur.fetchone() == None:
            con.close()
            return False
        else:
            con.close()
            return True

