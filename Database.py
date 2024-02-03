from googleapiclient.discovery import build
import sqlite3
import random

def add_entries(email, urls, titles, notes):
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
                title TEXT,
                notes TEXT,  -- Corrected column name for notes
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
    for url, title, note in zip(urls, titles, notes):
        cursor.execute('''
            INSERT INTO youtube_videos (url, title, notes, email, note_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (url, title, note, email, max_note_id))
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()


def get_random_entries(email, num_entries):
    # Connect to the SQLite database
    conn = sqlite3.connect('youtube_data.db')
    cursor = conn.cursor()
    
    # Check if the email exists in the table
    cursor.execute('''
        SELECT * FROM youtube_videos WHERE email = ?
    ''', (email,))
    rows = cursor.fetchall()
    
    if not rows:
        print("Email not found in the database.")
        return []
    
    # Shuffle the rows and select random entries up to num_entries
    random.shuffle(rows)
    selected_entries = rows[:num_entries]
    
    # Close the connection
    conn.close()
    
    # Convert selected entries to list of dictionaries
    entries_list = []
    for entry in selected_entries:
        entry_dict = {
            "url": entry[1],  # URL is at index 1
            "title": entry[2],  # Title is at index 2
            "notes": entry[3]  # Notes is at index 3
        }
        entries_list.append(entry_dict)
    
    return entries_list


def delete_and_create_table():
    conn = sqlite3.connect('youtube_data.db')
    cursor = conn.cursor()

    # Delete the existing table if it exists
    cursor.execute('''
        DROP TABLE IF EXISTS youtube_videos
    ''')

    # Create a new table with the required columns
    cursor.execute('''
        CREATE TABLE youtube_videos (
            id INTEGER PRIMARY KEY,
            url TEXT,
            title TEXT,
            notes TEXT,
            email TEXT,
            note_id INTEGER
        )
    ''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

#------------------------------------------------------TESTS-------------------------------------------------#

# Sample tests for add_entries function
def test_add_entries():
    # Test case 1: Adding entries for a new email
    email1 = 'test1@example.com'
    urls1 = ['url1', 'url2', 'url3']
    titles1 = ['title1', 'title2', 'title3']
    notes1 = ['note1', 'note2', 'note3']
    add_entries(email1, urls1, titles1, notes1)
    
    # Test case 2: Adding entries for an existing email
    email2 = 'test2@example.com'
    urls2 = ['url4', 'url5']
    titles2 = ['title4', 'title5']
    notes2 = ['note4', 'note5']
    add_entries(email2, urls2, titles2, notes2)
    
    # Test case 3: Adding entries for an existing email with existing entries
    urls3 = ['url6']
    titles3 = ['title6']
    notes3 = ['note6']
    add_entries(email1, urls3, titles3, notes3)
    
    # Test case 4: Adding entries for a non-existing email
    email4 = 'test4@example.com'
    urls4 = ['url7']
    titles4 = ['title7']
    notes4 = ['note7']
    add_entries(email4, urls4, titles4, notes4)

# Sample tests for get_random_entries function
def test_get_random_entries():
    # Test case 1: Getting random entries for an existing email with enough entries
    email1 = 'test1@example.com'
    num_entries1 = 2
    random_entries1 = get_random_entries(email1, num_entries1)
    print("Random entries for email 1:", random_entries1)
    
    # Test case 2: Getting random entries for an existing email with fewer entries than requested
    email2 = 'test2@example.com'
    num_entries2 = 5
    random_entries2 = get_random_entries(email2, num_entries2)
    print("Random entries for email 2:", random_entries2)
    
    # Test case 3: Getting random entries for a non-existing email
    email3 = 'test3@example.com'
    num_entries3 = 3
    random_entries3 = get_random_entries(email3, num_entries3)
    print("Random entries for email 3:", random_entries3)



# Run sample tests
# delete_and_create_table()
# test_add_entries()
# test_get_random_entries()



