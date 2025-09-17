import pdfplumber
import os
import re

folder_path = "invoices"

# Regex patterns
invoice_no_pattern = re.compile(r"Invoice No:\s*(\S+)")
date_pattern = re.compile(r"Date:\s*([\d-]+)")
total_pattern = re.compile(r"Total:\s*(\d+)")

for file_name in os.listdir(folder_path):
    if file_name.endswith(".pdf"):
        file_path = os.path.join(folder_path, file_name)
        print(f"\n🔹 Reading: {file_name}")

        with pdfplumber.open(file_path) as pdf:
            full_text = ""
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    full_text += text + "\n"

            # Match patterns
            invoice_no = invoice_no_pattern.search(full_text)
            date = date_pattern.search(full_text)
            total = total_pattern.search(full_text)

            print("Invoice No:", invoice_no.group(1) if invoice_no else "Not found")
            print("Date:", date.group(1) if date else "Not found")
            print("Total:", total.group(1) if total else "Not found")
