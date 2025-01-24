import sqlite3 as sql

db_path = "./.databaseFiles/database.db"

def insertUser(username, hashed_password, totp_secret):
    con = sql.connect(db_path)
    cur = con.cursor()
    # Check if the username already exists
    cur.execute("SELECT COUNT(*) FROM secure_users_9f WHERE username = ?", (username,))
    if cur.fetchone()[0] > 0:
        con.close()
        raise Exception("Username already exists")
    cur.execute(
        "INSERT INTO secure_users_9f (username, password, totp_secret) VALUES (?, ?, ?)",  
        (username, hashed_password, totp_secret),   
    )
    con.commit()
    con.close()

def retrieveUserByUsername(username):
    conn = sql.connect(db_path)
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM secure_users_9f WHERE username = ?",
        (username,)
    )
    user = cur.fetchone()
    conn.close()
    if user:
        return {
            'id': user[0],
            'username': user[1],
            'password': user[2],
            'totp_secret': user[3]  # Assuming the totp_secret is stored in the 4th column
        }
    return None

def updateUserTotpSecret(username, totp_secret):
    conn = sql.connect(db_path)
    cur = conn.cursor()
    cur.execute(
        "UPDATE secure_users_9f SET totp_secret = ? WHERE username = ?",
        (totp_secret, username)
    )
    conn.commit()
    conn.close()

def insertLogEntry(developer, project, start_time, end_time, time_worked, repo, developer_notes, developer_code):
    con = sql.connect(db_path)
    cur = con.cursor()
    cur.execute(
        "INSERT INTO log_entries_9f3b2 (developer, project, start_time, end_time, time_worked, repo, developer_notes, developer_code) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (developer, project, start_time, end_time, time_worked, repo, developer_notes, developer_code),
    )
    con.commit()
    con.close()

def retrieveLogEntries():
    conn = sql.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT * FROM log_entries_9f3b2")
    rows = cur.fetchall()
    conn.close()
    log_entries = []
    for row in rows:
        log_entries.append({
            'developer': row[1],
            'project': row[2],
            'start_time': row[3],
            'end_time': row[4],
            'time_worked': row[5],
            'repo': row[6],
            'developer_notes': row[7],
            'developer_code': row[8]
        })
    return log_entries