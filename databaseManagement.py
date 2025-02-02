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
            'totp_secret': user[3] 
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

def insertLogEntry(developer, project, start_time, end_time, time_worked, repo, developer_notes, developer_code, diary_entry):
    con = sql.connect(db_path)
    cur = con.cursor()
    cur.execute(
        "INSERT INTO log_entries_9f3b2 (developer, project, start_time, end_time, time_worked, repo, developer_notes, developer_code, diary_entry) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (developer, project, start_time, end_time, time_worked, repo, developer_notes, developer_code, diary_entry),
    )
    con.commit()
    con.close()

def retrieveLogEntries(query=None, category=None):
    conn = sql.connect(db_path)
    cur = conn.cursor()
    if query and category:
        query = f"%{query}%"
        allowed_categories = ["developer", "project", "developer_notes", "developer_code"]  # List of allowed column names
        if category in allowed_categories:
            sql_query = f"SELECT * FROM log_entries_9f3b2 WHERE {category} LIKE ?"
            cur.execute(sql_query, (query,))
        else:
            raise ValueError("Invalid category")
    else:
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
            'developer_code': row[8],
            'diary_entry': row[9]
        })
    return log_entries

def retrieveUserData(username):
    conn = sql.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT * FROM secure_users_9f WHERE username = ?", (username,))
    user = cur.fetchone()
    cur.execute("SELECT * FROM log_entries_9f3b2 WHERE developer = ?", (username,))
    log_entries = cur.fetchall()
    conn.close()
    if user:
        user_data = {
            'id': user[0],
            'username': user[1],
            'password': user[2],
            'totp_secret': user[3],
            'log_entries': []
        }
        for entry in log_entries:
            user_data['log_entries'].append({
                'id': entry[0],
                'developer': entry[1],
                'project': entry[2],
                'start_time': entry[3],
                'end_time': entry[4],
                'time_worked': entry[5],
                'repo': entry[6],
                'developer_notes': entry[7],
                'developer_code': entry[8],
                'diary_entry': entry[9]
            })
        return user_data
    return None

def deleteUserData(username):
    conn = sql.connect(db_path)
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM log_entries_9f3b2 WHERE developer = ?", (username,))
        cur.execute("DELETE FROM secure_users_9f WHERE username = ?", (username,))
        conn.commit()
        conn.close()
        return True
    except sql.Error as e:
        conn.rollback()
        conn.close()
        return False