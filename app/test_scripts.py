from app.task_queue.tasks.run_scrape_task import run_scrape_task
from app.core.datastore.local_database import LocalDatabase

local_db = LocalDatabase()
db_connection = local_db.get_connection()

run_scrape_task(4,None, db_connection)