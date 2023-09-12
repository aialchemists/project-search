from core.db import DB
from utils.configs import db_configs
from utils.commons import print_line

print("Starting database migration - Connection details :" + db_configs.get_dsn())
print_line()

db = DB()
schema = db.migrate()
print(f"Schema: {schema}")

print_line()
print("DB migration complete!")
