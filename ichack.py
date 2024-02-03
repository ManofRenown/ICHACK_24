from googleapiclient.discovery import build
import sqlite3

def add_entries(email, urls, notes):
    # Connect to the SQLite database
    conn = sqlite3.connect('youtube_data.db')
    cursor = conn.cursor()
    
    # Check if the table exists
    cursor.execute('''
        SELECT name FROM sqlite_master WHERE type='table' AND name='youtube_videos'
    ''')
    table_exists = cursor.fetchone() is not None
    
    # If the table doesn't exist, create it
    if not table_exists:
        cursor.execute('''
            CREATE TABLE youtube_videos (
                id INTEGER PRIMARY KEY,
                url TEXT,
                notes TEXT,
                email TEXT,
                note_id INTEGER
            )
        ''')
        max_note_id = 0
    else:
        # Check if the email already exists in the table
        cursor.execute('''
            SELECT MAX(note_id) FROM youtube_videos WHERE email = ?
        ''', (email,))
        max_note_id = cursor.fetchone()[0]
        
        # If the email exists, increment the max note_id by 1, otherwise start from 1
        if max_note_id is None:
            max_note_id = 0
        else:
            max_note_id += 1
    
    # Insert entries into the table with the same note_id
    for url, note in zip(urls, notes):
        cursor.execute('''
            INSERT INTO youtube_videos (url, notes, email, note_id)
            VALUES (?, ?, ?, ?)
        ''', (url, note, email, max_note_id))
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()
