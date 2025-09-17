import sqlite3

DB_NAME = "invoices.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS invoices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_no TEXT UNIQUE,
            date TEXT,
            client TEXT,
            total TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_invoice(invoice_no, date, client, total):
    # --- Validation checks ---
    if not invoice_no or invoice_no == "Not found":
        print(f"⚠️ Skipped: Missing Invoice No")
        return False
    if not date or date == "Not found":
        print(f"⚠️ Skipped: Missing Date for invoice {invoice_no}")
        return False
    if not client or client == "Not found":
        print(f"⚠️ Skipped: Missing Client for invoice {invoice_no}")
        return False
    if not total or total == "Not found":
        print(f"⚠️ Skipped: Missing Total for invoice {invoice_no}")
        return False

    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute(
            "INSERT INTO invoices (invoice_no, date, client, total) VALUES (?, ?, ?, ?)",
            (invoice_no, date, client, total)
        )
        conn.commit()
        conn.close()
        print(f"✅ Saved invoice {invoice_no} to database.")
        return True
    except sqlite3.IntegrityError:
        print(f"⚠️ Duplicate invoice detected: {invoice_no}")
        return False

def fetch_all_invoices():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT invoice_no, date, client, total FROM invoices")
    rows = c.fetchall()
    conn.close()
    return rows

if __name__ == "__main__":
    init_db()
    print("✅ Database initialized with invoices table")
