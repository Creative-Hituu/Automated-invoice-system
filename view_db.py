import sqlite3

def view_invoices():
    conn = sqlite3.connect("invoices.db")
    cursor = conn.cursor()

    # Table se data nikalna
    cursor.execute("SELECT * FROM invoices")
    rows = cursor.fetchall()

    print("📋 Invoices Table Data:\n")
    print("ID | Invoice No | Date | Vendor | Total")
    print("-" * 50)
    for row in rows:
        print(row)

    conn.close()

if __name__ == "__main__":
    view_invoices()
