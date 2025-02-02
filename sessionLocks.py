import threading
from flask import session

# Global dictionary to store locks
session_locks = {}

# Function to get or create a lock for a session
def get_session_lock(session_id):
    if session_id not in session_locks:
        session_locks[session_id] = threading.Lock()
    return session_locks[session_id]

# Cleanup function to remove the lock when the session is deleted
def cleanup_session_lock(response):
    session_id = session.sid
    if session_id in session_locks:
        del session_locks[session_id]
    return response

# Function to acquire the session lock
def acquire_session_lock():
    session_id = session.sid
    lock = get_session_lock(session_id)
    return lock


