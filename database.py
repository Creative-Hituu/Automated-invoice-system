import sqlite3

# Database connection (agar file nahi hai to automatic create ho jayegi)
conn = sqlite3.connect("invoices.db")
cursor = conn.cursor()

# Invoice table banate hain
cursor.execute("""
CREATE TABLE IF NOT EXISTS invoices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    invoice_number TEXT,
    date TEXT,
    vendor TEXT,
    total REAL
)
""")

print("✅ Database aur table create ho gaya.")

conn.commit()
conn.close()
