import pdfplumber
import os
import re
import pandas as pd

folder_path = "invoices"

# Regex patterns
invoice_no_pattern = re.compile(r"Invoice No:\s*(\S+)")
date_pattern = re.compile(r"Date:\s*([\d-]+)")
total_pattern = re.compile(r"Total:\s*(\d+)")
gst_pattern = re.compile(r"GST.*?:\s*(\d+)")

summary_data = []
items_data = []

for file_name in os.listdir(folder_path):
    if file_name.endswith(".pdf"):
        file_path = os.path.join(folder_path, file_name)

        with pdfplumber.open(file_path) as pdf:
            full_text = ""
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    full_text += text + "\n"

            # Extract values
            invoice_no = invoice_no_pattern.search(full_text)
            date = date_pattern.search(full_text)
            total = total_pattern.search(full_text)
            gst = gst_pattern.search(full_text)

            # Client info
            client_name, client_address = "Not found", "Not found"
            lines = full_text.splitlines()
            for i, line in enumerate(lines):
                if line.strip().startswith("Bill To:"):
                    if i+1 < len(lines):
                        client_name = lines[i+1].strip()
                    if i+2 < len(lines):
                        client_address = lines[i+2].strip()
                    break

            # Summary row
            summary_data.append({
                "File Name": file_name,
                "Invoice No": invoice_no.group(1) if invoice_no else "Not found",
                "Date": date.group(1) if date else "Not found",
                "Client Name": client_name,
                "Client Address": client_address,
                "GST": gst.group(1) if gst else "Not found",
                "Total": total.group(1) if total else "Not found"
            })

            # Items rows
            for line in lines:
                match = re.match(r"(.+?)\s+(\d+)\s+(\d+)\s+(\d+)", line.strip())
                if match:
                    description, qty, rate, amount = match.groups()
                    items_data.append({
                        "Invoice No": invoice_no.group(1) if invoice_no else "Not found",
                        "Description": description.strip(),
                        "Qty": qty,
                        "Rate": rate,
                        "Amount": amount
                    })

# Save to Excel with 2 sheets
with pd.ExcelWriter("invoices_full.xlsx") as writer:
    pd.DataFrame(summary_data).to_excel(writer, sheet_name="Invoice Summary", index=False)
    pd.DataFrame(items_data).to_excel(writer, sheet_name="Invoice Items", index=False)

print("✅ Excel file generated with 2 sheets: invoices_full.xlsx")
