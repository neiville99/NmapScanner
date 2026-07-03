import sqlite3
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "scans.db"

def create_db() -> None:
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scans (
            scan_id INTEGER PRIMARY KEY AUTOINCREMENT,
            scan_target TEXT NOT NULL,
            scan_time TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scan_results (
            result_id INTEGER PRIMARY KEY AUTOINCREMENT,
            scan_id INTEGER NOT NULL,
            host TEXT NOT NULL,
            hostname TEXT,
            port INTEGER NOT NULL,
            protocol TEXT,
            state TEXT,
            service TEXT,
            product TEXT,
            version TEXT,
            FOREIGN KEY (scan_id) REFERENCES scans(scan_id)
        )
    """)

    connection.commit()
    connection.close()

    print("Database ready")

def save_scan_records(scan_target: str, records: list[dict]) -> int:
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    scan_time = datetime.now().isoformat(timespec="seconds")

    cursor.execute("""
        INSERT INTO scans (
            scan_target,
            scan_time
        )
        VALUES (?, ?)
    """, (
        scan_target,
        scan_time
    ))

    scan_id = cursor.lastrowid

    for record in records:
        cursor.execute("""
            INSERT INTO scan_results (
                scan_id,
                host,
                hostname,
                port,
                protocol,
                state,
                service,
                product,
                version
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            scan_id,
            record.get("host", ""),
            record.get("hostname", ""),
            record.get("port", 0),
            record.get("protocol", ""),
            record.get("state", ""),
            record.get("service", ""),
            record.get("product", ""),
            record.get("version", "")
        ))

    connection.commit()
    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        ORDER BY name
    """)

    tables = cursor.fetchall()
    print(f"db path: {DATABASE_PATH}")
    print("Tables:", tables)
    connection.close()

    print(f"Saved scan {scan_id} with {len(records)} port records")

    return scan_id