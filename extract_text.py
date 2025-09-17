import pdfplumber
import os

# Invoice folder ka path
folder_path = "invoices"

# Sare PDF files loop karna
for file_name in os.listdir(folder_path):
    if file_name.endswith(".pdf"):
        file_path = os.path.join(folder_path, file_name)
        print(f"\n🔹 Reading: {file_name}")

        # PDF open karo aur text nikaalo
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    print(text)
