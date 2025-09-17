# 📑 Automated Invoice Processing System  

--> An end-to-end **Automated Invoice Management System** built with **Python, Tkinter, SQLite, and PDF processing tools**.  <br>
--> This project automatically extracts invoice data from PDFs, stores them in a database, and provides options to **view, export, and manage invoices** with a user-friendly interface.  

---

## 🚀 Features
- 📂 Upload multiple invoices (PDFs) at once  
- ⚡ Automatic extraction of:
  - Invoice Number  
  - Date  
  - Client Name  
  - Total Amount  
- 🗄 Save all invoice data into a **SQLite database**  
- 👀 View all processed invoices in an interactive table  
- 📤 Export invoices to **Excel (.xlsx)** or **CSV** format  
- ✅ Duplicate invoice check (prevents storing same invoice twice)  
- 🎨 Simple & clean **Tkinter GUI**  

---

## 🛠 Tech Stack
- **Python 3.x**  
- **Tkinter** (for GUI)  
- **SQLite3** (database)  
- **pdfplumber** (PDF data extraction)  
- **openpyxl / pandas** (Excel & CSV export)

---

## ⚙️ Installation  

1. Clone the repository  
   ```bash
   git clone https://github.com/Creative-Hituu/Automated-invoice-system.git
   cd Automated-invoice-system
2. Create a virtual environment
   ```base
   python -m venv venv
   venv\Scripts\activate   # For Windows
   source venv/bin/activate  # For Linux/Mac
3. Install dependencies
   ```base
   pip install -r requirements.txt
4. Run the app
   ```base
   python app.py

---

## 📂 Project Structure
    ```text
    Automated-invoice-system/
    ├── app.py              # Main GUI application
    ├── batch_process.py    # Handles invoice extraction + Excel export
    ├── db_utils.py         # Database setup and queries
    ├── invoices/           # Folder where uploaded invoice PDFs are stored
    ├── all_invoices.xlsx   # Auto-generated summary file
    └── README.md           # Project documentation

---

## 📬 Contact Me

👤 **Hitanshu Prajapati**  
📧 Email: hitanshubro1@gmail.com  
🔗 [LinkedIn Profile](https://www.linkedin.com/in/hitanshu-prajapati-hi)  
💻 [GitHub Profile](https://github.com/Creative-Hituu)


