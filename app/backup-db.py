import sqlite3
import logging
import os
import os.path
from datetime import datetime
from cryptic.settings import DB_DIR

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

log = logging.getLogger("DB_BACKUP")

log.info("Starting DB backup")

MAX_BACKUPS = 10

DB_NAME = "db.sqlite3"
DB_PATH = os.path.join(DB_DIR, DB_NAME)

BACKUP_DIR = os.path.join(DB_DIR, "backups")
log.debug("BACKUP DIR : %s", BACKUP_DIR)
log.debug("DB PATH : %s", DB_PATH)

if not os.path.exists(BACKUP_DIR):
    log.info("Creating backup dir : %s", BACKUP_DIR)
    os.mkdir(BACKUP_DIR)

current_backups = [file for file in os.listdir(BACKUP_DIR) if os.path.isfile(file)]
log.debug("Current backups : %s", current_backups)

if len(current_backups) > MAX_BACKUPS:
    current_backups = sorted(current_backups, reverse=True)
    for backup_file in current_backups[:-MAX_BACKUPS]:
        log.info("Deleting : %s", backup_file)
        try:
            os.unlink(backup_file)
        except Exception:
            pass


conn = sqlite3.connect(DB_PATH)

BACKUP_NAME = f"backup-{datetime.utcnow().strftime('%Y-%m-%d-%H-%M')}.sqlite3"
BACKUP_PATH = os.path.join(BACKUP_DIR, BACKUP_NAME)
log.debug("BACKUP PATH : %s", BACKUP_PATH)

backup = sqlite3.connect(BACKUP_PATH)

try:
    log.info("Backing up database")
    with backup:
        conn.backup(backup, pages=1)

except Exception as e:
    log.exception("Exception while backup : %s", e)

finally:
    conn.close()
    backup.close()