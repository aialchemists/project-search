from utils.logger import log, print_line
import db
import apis.elastic_search as elastic_search

try:
  db.init()
  elastic_search.init()
except Exception as exc:
  log.error("Exception while initialising DB migrate service", exc)

log.info("Starting database migration")
print_line()

schema = db.migrate()
print(f"Schema:\n{schema}")

elastic_search.migrate()

print_line()
log.info("DB migration complete!")
