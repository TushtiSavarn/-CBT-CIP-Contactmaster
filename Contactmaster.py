import mysql.connector
import ttkbootstrap as ttk
from tkinter import *
from ttkbootstrap import Style
from tkinter import messagebox

class ContactMaster:
    def __init__(self, root):
        self.root = root
        self.root.title("ContactMaster - Contact Management System")
        self.root.geometry("700x500")
        
        # Apply modern UI theme
        self.style = Style(theme="superhero")

        # MySQL Connection
        self.conn = mysql.connector.connect(host="localhost", user="root", password="", database="contact_db")
        self.cursor = self.conn.cursor()

        # UI Components
        self.setup_ui()

    def setup_ui(self):
        Label(self.root, text="Contact Management System", font=("Helvetica", 18, "bold")).pack(pady=10)

        # Form Fields
        frame = ttk.Frame(self.root, padding=10)
        frame.pack(pady=10)

        ttk.Label(frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = ttk.Entry(frame, width=30)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Address:").grid(row=1, column=0, padx=5, pady=5)
        self.address_entry = ttk.Entry(frame, width=30)
        self.address_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Phone Number:").grid(row=2, column=0, padx=5, pady=5)
        self.phone_entry = ttk.Entry(frame, width=30)
        self.phone_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Email:").grid(row=3, column=0, padx=5, pady=5)
        self.email_entry = ttk.Entry(frame, width=30)
        self.email_entry.grid(row=3, column=1, padx=5, pady=5)

        # Buttons
        button_frame = ttk.Frame(self.root, padding=10)
        button_frame.pack()

        ttk.Button(button_frame, text="Add Contact", command=self.add_contact, bootstyle="success").grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(button_frame, text="Update Contact", command=self.update_contact, bootstyle="warning").grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(button_frame, text="Delete Contact", command=self.delete_contact, bootstyle="danger").grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(button_frame, text="Search Contact", command=self.search_contact, bootstyle="primary").grid(row=0, column=3, padx=5, pady=5)

        # Contact List
        self.contact_list = ttk.Treeview(self.root, columns=("Name", "Address", "Phone", "Email"), show="headings")
        self.contact_list.heading("Name", text="Name")
        self.contact_list.heading("Address", text="Address")
        self.contact_list.heading("Phone", text="Phone Number")
        self.contact_list.heading("Email", text="Email")
        self.contact_list.pack(pady=10)
        
        self.load_contacts()

    def add_contact(self):
        name = self.name_entry.get()
        address = self.address_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()

        if name and address and phone and email:
            try:
                self.cursor.execute("INSERT INTO contacts (name, address, phone_number, email) VALUES (%s, %s, %s, %s)", 
                                    (name, address, phone, email))
                self.conn.commit()
                messagebox.showinfo("Success", "Contact Added Successfully!")
                self.clear_fields()
                self.load_contacts()
            except mysql.connector.IntegrityError:
                messagebox.showerror("Error", "Phone number already exists!")
        else:
            messagebox.showwarning("Warning", "All fields are required!")

    def update_contact(self):
        selected_item = self.contact_list.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a contact to update!")
            return

        name = self.name_entry.get()
        address = self.address_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()

        if name and address and phone and email:
            self.cursor.execute("UPDATE contacts SET name=%s, address=%s, email=%s WHERE phone_number=%s", 
                                (name, address, email, phone))
            self.conn.commit()
            messagebox.showinfo("Success", "Contact Updated Successfully!")
            self.clear_fields()
            self.load_contacts()
        else:
            messagebox.showwarning("Warning", "All fields are required!")

    def delete_contact(self):
        selected_item = self.contact_list.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a contact to delete!")
            return
        
        phone = self.contact_list.item(selected_item, "values")[2]  # Get phone number
        self.cursor.execute("DELETE FROM contacts WHERE phone_number=%s", (phone,))
        self.conn.commit()
        messagebox.showinfo("Success", "Contact Deleted Successfully!")
        self.load_contacts()

    def search_contact(self):
        query = self.name_entry.get()
        if query:
            self.cursor.execute("SELECT name, address, phone_number, email FROM contacts WHERE name LIKE %s", 
                                (f"%{query}%",))
            results = self.cursor.fetchall()
            self.contact_list.delete(*self.contact_list.get_children())
            for row in results:
                self.contact_list.insert("", "end", values=row)
        else:
            messagebox.showwarning("Warning", "Enter a name to search!")

    def load_contacts(self):
        self.contact_list.delete(*self.contact_list.get_children())  # Clear list
        self.cursor.execute("SELECT name, address, phone_number, email FROM contacts")
        contacts = self.cursor.fetchall()
        for row in contacts:
            self.contact_list.insert("", "end", values=row)

    def clear_fields(self):
        self.name_entry.delete(0, END)
        self.address_entry.delete(0, END)
        self.phone_entry.delete(0, END)
        self.email_entry.delete(0, END)

# Start the Application
if __name__ == "__main__":
    root = ttk.Window(themename="superhero")  # Initialize window with modern theme
    app = ContactMaster(root)
    root.mainloop()
