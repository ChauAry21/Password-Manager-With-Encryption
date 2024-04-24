import tkinter as tk
from tkinter import simpledialog
from cryptography.fernet import Fernet
import mysql.connector
import uuid

class PasswordManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Manager")

        # Connect to MySQL database
        self.conn = mysql.connector.connect(
            host="your_mysql_host",
            user="your_mysql_username",
            password="your_mysql_password",
            database="secure_keys"
        )

        # GUI elements
        self.label = tk.Label(self.root, text="Welcome to Aryan's Password Manager!")
        self.label.pack()

        self.search_button = tk.Button(self.root, text="Search Existing Entry", command=self.search_entry)
        self.search_button.pack()

        self.new_button = tk.Button(self.root, text="Create New Entry", command=self.create_entry)
        self.new_button.pack()

        self.output_text = tk.Text(self.root, wrap=tk.WORD, width=40, height=10)
        self.output_text.pack()

    def search_entry(self):
        mac_address = self.get_mac_address()
        if mac_address:
            cursor = self.conn.cursor()
            cursor.execute("SELECT encryption_key FROM mac_addresses WHERE mac_address=%s", (mac_address,))
            row = cursor.fetchone()
            if row:
                key = row[0]
                encrypted_data = self.read_from_file("encrypted_data.txt")
                decrypted_data = self.decrypt_message(encrypted_data, key)
                self.output_text.delete(1.0, tk.END)
                self.output_text.insert(tk.END, decrypted_data)
            else:
                self.output_text.insert(tk.END, "No key found for the specified MAC address.\n")

    def create_entry(self):
        mac_address = self.get_mac_address()
        if mac_address:
            key = self.show_popup("Create New Entry", "Enter encryption key:")
            if key:
                cursor = self.conn.cursor()
                cursor.execute("INSERT INTO mac_addresses (mac_address, encryption_key) VALUES (%s, %s)",
                               (mac_address, key))
                self.conn.commit()
                self.output_text.delete(1.0, tk.END)
                self.output_text.insert(tk.END, "New entry created and saved successfully.\n")

    def get_mac_address():
        mac = uuid.getnode()
        mac_address = ':'.join(['{:02x}'.format((mac >> elements) & 0xff) for elements in range(0,2*6,2)])
        return mac_address


    def show_popup(self, title, message):
        return simpledialog.askstring(title, message)

    def decrypt_message(self, encrypted_message, key):
        cipher_suite = Fernet(key)
        decrypted_message = cipher_suite.decrypt(encrypted_message).decode()
        return decrypted_message

    def read_from_file(self, filename):
        try:
            with open(filename, 'rb') as file:
                data = file.read()
            return data
        except FileNotFoundError:
            return b''

def main():
    root = tk.Tk()
    root.geometry("400x300")
    app = PasswordManagerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
