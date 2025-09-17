import os
import pdfplumber
import re
import openpyxl
from db_utils import save_invoice, init_db

# invoices folder ka path
folder_path = "invoices"

def extract_invoice_data(pdf_path):
    """Extract invoice details from a PDF using regex."""
    with pdfplumber.open(pdf_path) as pdf:
        full_text = ""
        for page in pdf.pages:
            full_text += (page.extract_text() or "") + "\n"

    # Regex extraction
    invoice_number = re.search(r"Invoice\s*[:\-]?\s*(\S+)", full_text, re.IGNORECASE)
    date_val = re.search(r"(?:Date|Invoice Date)\s*[:\-]?\s*(\S+)", full_text, re.IGNORECASE)
    client_name = re.search(r"(?:Client|Customer|Billed To)\s*[:\-]?\s*(.+)", full_text, re.IGNORECASE)
    total_val = re.search(r"(?:Total|Grand Total)\s*[:\-]?\s*(\d+(?:\.\d{1,2})?)", full_text, re.IGNORECASE)

    return (
        invoice_number.group(1).strip() if invoice_number else "Not found",
        date_val.group(1).strip() if date_val else "Not found",
        client_name.group(1).strip() if client_name else "Not found",
        total_val.group(1).strip() if total_val else "Not found"
    )

def process_invoices():
    """Process invoices from invoices folder, save to DB + Excel."""
    init_db()  # make sure DB and table exist
    summary_data = []

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    for file in os.listdir(folder_path):
        if file.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, file)
            try:
                invoice_no, date_val, client_name, total_val = extract_invoice_data(pdf_path)

                # save to DB with validation
                save_invoice(invoice_no, date_val, client_name, total_val)
                summary_data.append((invoice_no, date_val, client_name, total_val))
                print(f"✅ Saved invoice {invoice_no} to database.")
            except Exception as e:
                print(f"❌ Error processing {file}: {e}")

    # Export to Excel
    if summary_data:
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Invoices"
        ws.append(["Invoice No", "Date", "Client", "Total"])
        for row in summary_data:
            ws.append(row)
        wb.save("all_invoices.xlsx")
        print("✅ All invoices processed successfully into all_invoices.xlsx and saved to database")

    return summary_data  # so GUI can directly use it

if __name__ == "__main__":
    process_invoices()
