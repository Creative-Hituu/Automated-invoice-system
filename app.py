import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import pandas as pd
from batch_process import folder_path, process_invoices
from db_utils import fetch_all_invoices

class InvoiceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📑 Automated Invoice Processing System")
        self.root.geometry("900x600")
        self.root.config(bg="#f4f6f7")

        # ---- Title ----
        title_label = tk.Label(
            root,
            text="Automated Invoice Processing System",
            font=("Arial", 18, "bold"),
            fg="#2c3e50",
            bg="#f4f6f7"
        )
        title_label.pack(pady=15)

        # ---- Buttons Frame ----
        btn_frame = tk.Frame(root, bg="#f4f6f7")
        btn_frame.pack(pady=10)

        upload_btn = tk.Button(
            btn_frame,
            text="📂 Upload Invoices",
            command=self.upload_invoices,
            font=("Arial", 12),
            bg="#3498db",
            fg="white",
            padx=10,
            pady=5
        )
        upload_btn.grid(row=0, column=0, padx=10)

        process_btn = tk.Button(
            btn_frame,
            text="⚡ Process Invoices",
            command=self.process_invoices,
            font=("Arial", 12),
            bg="#27ae60",
            fg="white",
            padx=10,
            pady=5
        )
        process_btn.grid(row=0, column=1, padx=10)

        export_btn = tk.Button(
            btn_frame,
            text="📤 Export Data",
            command=self.export_data,
            font=("Arial", 12),
            bg="#f39c12",
            fg="white",
            padx=10,
            pady=5
        )
        export_btn.grid(row=0, column=2, padx=10)

        view_btn = tk.Button(
            btn_frame,
            text="👁 View Invoice",
            command=self.view_invoice,
            font=("Arial", 12),
            bg="#8e44ad",
            fg="white",
            padx=10,
            pady=5
        )
        view_btn.grid(row=0, column=3, padx=10)

        exit_btn = tk.Button(
            btn_frame,
            text="❌ Exit",
            command=root.quit,
            font=("Arial", 12),
            bg="#e74c3c",
            fg="white",
            padx=10,
            pady=5
        )
        exit_btn.grid(row=0, column=4, padx=10)

        # ---- Treeview Table ----
        self.tree = ttk.Treeview(root, columns=("Invoice No", "Date", "Client", "Total"), show="headings", height=15)
        self.tree.heading("Invoice No", text="Invoice No")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Client", text="Client")
        self.tree.heading("Total", text="Total")
        self.tree.pack(pady=20, fill="x")

        # Scrollbar
        scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

    def upload_invoices(self):
        files = filedialog.askopenfilenames(title="Select Invoice PDFs", filetypes=[("PDF Files", "*.pdf")])
        if files:
            for f in files:
                try:
                    dest = os.path.join(folder_path, os.path.basename(f))
                    if os.path.abspath(f) != os.path.abspath(dest):  # prevent same-path issue
                        os.replace(f, dest)
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to move file {f}\n{e}")
            messagebox.showinfo("Upload Complete", "Invoices uploaded successfully!")

    def process_invoices(self):
        process_invoices()  # process and save to DB
        self.tree.delete(*self.tree.get_children())  
        rows = fetch_all_invoices()
        if rows:
            for row in rows:
                self.tree.insert("", "end", values=row)
            messagebox.showinfo("Processing", f"{len(rows)} invoices loaded from database!")
        else:
            messagebox.showwarning("No Data", "No invoices found in database.")

    def export_data(self):
        rows = fetch_all_invoices()
        if not rows:
            messagebox.showwarning("No Data", "No invoices to export!")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                 filetypes=[("Excel Files", "*.xlsx"), ("CSV Files", "*.csv")])
        if not file_path:
            return

        df = pd.DataFrame(rows, columns=["Invoice No", "Date", "Client", "Total"])
        if file_path.endswith(".csv"):
            df.to_csv(file_path, index=False)
        else:
            df.to_excel(file_path, index=False)

        messagebox.showinfo("Export Complete", f"Data exported successfully to {file_path}")

    def view_invoice(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select an invoice to view.")
            return

        values = self.tree.item(selected_item, "values")
        if not values:
            messagebox.showerror("Error", "Could not fetch invoice details.")
            return

        invoice_no, date, client, total = values

        # Popup Window
        win = tk.Toplevel(self.root)
        win.title(f"Invoice Details - {invoice_no}")
        win.geometry("400x300")
        win.config(bg="#ecf0f1")

        tk.Label(win, text=f"📄 Invoice No: {invoice_no}", font=("Arial", 14, "bold"), bg="#ecf0f1").pack(pady=10)
        tk.Label(win, text=f"📅 Date: {date}", font=("Arial", 12), bg="#ecf0f1").pack(pady=5)
        tk.Label(win, text=f"👤 Client: {client}", font=("Arial", 12), bg="#ecf0f1").pack(pady=5)
        tk.Label(win, text=f"💰 Total: {total}", font=("Arial", 12, "bold"), fg="green", bg="#ecf0f1").pack(pady=10)

        close_btn = tk.Button(win, text="Close", command=win.destroy, bg="#e74c3c", fg="white", padx=10, pady=5)
        close_btn.pack(pady=15)


if __name__ == "__main__":
    root = tk.Tk()
    app = InvoiceApp(root)
    root.mainloop()
