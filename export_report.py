from database import DEFAULT_DB, get_connection


def export_table_to_csv(table_name, csv_path, db_path=DEFAULT_DB):
    conn = get_connection(db_path)
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {table_name}")
    rows = cur.fetchall()
    headers = [d[0] for d in cur.description]
    conn.close()
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for r in rows:
            writer.writerow([r[h] for h in headers])
    return csv_path

