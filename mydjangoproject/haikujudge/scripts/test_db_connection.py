from django.db import connections
from django.db.utils import OperationalError

def run():
    db_conn = connections['default']
    try:
        c = db_conn.cursor()
    except OperationalError:
        raise OperationalError("Database connection failed")
    else:
        print("Database connection successful")