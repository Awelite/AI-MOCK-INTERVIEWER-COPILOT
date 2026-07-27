from coding_round.database import (
    get_db
)

conn = get_db()

print(
    "DB Connected Successfully"
)

conn.close()