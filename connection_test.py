from scripts.data_ingestion.sql_connection import get_connection


def main():
    try:
        conn = get_connection()
    except Exception as exc:
        print(f"Connection failed: {exc}")
        return

    cursor = conn.cursor()
    try:
        tables = ["dbo.demographic", "dbo.account", "dbo.location"]
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"{table}: {count} rows")

        cursor.execute("SELECT TOP 3 * FROM dbo.demographic")
        rows = cursor.fetchall()
        print(f"TOP 3 from dbo.demographic: {len(rows)} rows")
        for row in rows:
            print(row)
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    main()
