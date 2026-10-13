import sqlite3
import shutil
import os
import glob

history_paths = glob.glob(r"C:\Users\crypt\AppData\Local\Google\Chrome\User Data\*\History") + glob.glob(r"C:\Users\crypt\AppData\Local\Google\Chrome\User Data\Default\History")

for hp in set(history_paths):
    temp_db = hp + ".temp"
    try:
        shutil.copyfile(hp, temp_db)
        conn = sqlite3.connect(temp_db)
        cur = conn.cursor()
        cur.execute("SELECT url, title, last_visit_time FROM urls WHERE url LIKE '%docs.google.com/spreadsheets%' ORDER BY last_visit_time DESC LIMIT 10")
        rows = cur.fetchall()
        print(f"=== {hp} ===")
        for r in rows:
            print(r[0], "-->", r[1])
        conn.close()
        os.remove(temp_db)
    except Exception as e:
        print(f"Error for {hp}: {e}")
