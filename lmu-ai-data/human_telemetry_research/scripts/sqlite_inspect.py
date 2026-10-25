"""Read-only schema and row-count dump for a SQLite file (data, not code)."""
import os
import sqlite3
import sys

path = sys.argv[1]
uri = "file:" + os.path.abspath(path) + "?mode=ro&immutable=1"
con = sqlite3.connect(uri, uri=True)
cur = con.cursor()
objs = cur.execute(
    "select type, name, sql from sqlite_master where type in ('table','view') order by name"
).fetchall()
print(f"FILE {path} size={os.path.getsize(path)} objects={len(objs)}")
for kind, name, sql in objs:
    n = cur.execute(f'select count(*) from "{name}"').fetchone()[0]
    print(f"== {kind} {name} rows={n}")
    print("   " + (sql or "").replace("\n", " ")[:700])
    if n and len(sys.argv) > 2:
        cols = [c[1] for c in cur.execute(f'pragma table_info("{name}")').fetchall()]
        print("   cols:", cols)
        for row in cur.execute(f'select * from "{name}" limit 2').fetchall():
            print("   row:", [str(v)[:60] for v in row])
con.close()
