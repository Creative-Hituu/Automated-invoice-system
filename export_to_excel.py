import pdfplumber
import os
import re
import pandas as pd

folder_path = "invoices"

# Regex patterns
invoice_no_pattern = re.compile(r"Invoice No:\s*(\S+)")
date_pattern = re.compile(r"Date:\s*([\d-]+)")
total_pattern = re.compile(r"Total:\s*(\d+)")

data = []

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

            data.append({
                "File Name": file_name,
                "Invoice No": invoice_no.group(1) if invoice_no else "Not found",
                "Date": date.group(1) if date else "Not found",
                "Total": total.group(1) if total else "Not found"
            })

df = pd.DataFrame(data)

output_file = "invoices_summary.xlsx"
df.to_excel(output_file, index=False)

print(f"✅ Excel file generated: {output_file}")
