import sqlite3
import os
import os.path
from datetime import datetime
from app.cryptic.settings import DB_DIR

MAX_BACKUPS = 10

DB_NAME = "db.sqlite3"
DB_PATH = os.path.join(DB_DIR, DB_NAME)

BACKUP_DIR = os.path.join(DB_DIR, "backups")

if not os.path.exists(BACKUP_DIR):
    os.mkdir(BACKUP_DIR)

current_backups = [file for file in os.listdir(BACKUP_DIR) if os.path.isfile(file)]

if len(current_backups) > MAX_BACKUPS:
    current_backups = sorted(current_backups, reverse=True)
    for backup_file in current_backups[:-MAX_BACKUPS]:
        try:
            os.unlink(backup_file)
        except Exception:
            pass


conn = sqlite3.connect(DB_PATH)

BACKUP_NAME = f"backup-{datetime.utcnow().strftime('%Y-%m-%d-%H-%M')}.sqlite3"

backup = sqlite3.backup(BACKUP_NAME)

try:
    with backup:
        conn.backup(backup, pages=1)

except Exception as e:
    print("Exception while backup : ", e)

finally:
    conn.close()
    backup.close()