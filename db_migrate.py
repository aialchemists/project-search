from utils.logger import log, print_line
import utils.db as db

try:
  db.init()
except Exception as exc:
  log.error("Exception while initialising DB migrate service", exc)

log.info("Starting database migration")
print_line()

schema = db.migrate()
print(f"Schema:\n{schema}")

print_line()
log.info("DB migration complete!")
