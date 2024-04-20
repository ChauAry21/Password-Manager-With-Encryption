import tkinter as tk
from tkinter import simpledialog
from cryptography.fernet import Fernet
import os

class PasswordManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Manager")

        # Load or generate an encryption key
        self.key = self.load_or_generate_key()

        # GUI elements
        self.label = tk.Label(self.root, text="Welcome to Aryan's Password Manager!")
        self.label.pack()

        self.search_button = tk.Button(self.root, text="Search Existing Entry", command=self.search_entry)
        self.search_button.pack()

        self.new_button = tk.Button(self.root, text="Create New Entry", command=self.create_entry)
        self.new_button.pack()

        self.output_text = tk.Text(self.root, wrap=tk.WORD, width=40, height=10)
        self.output_text.pack()

    def load_or_generate_key(self):
        key_file = "key.txt"
        if os.path.exists(key_file):
            with open(key_file, 'rb') as file:
                return file.read()
        else:
            key = Fernet.generate_key()
            with open(key_file, 'wb') as file:
                file.write(key)
            return key

    def search_entry(self):
        website_name = self.show_popup("Search Existing Entry", "Enter website name:")
        if website_name:
            encrypted_data = self.read_from_file("encrypted_data.txt")
            found_entry = self.search_credentials(website_name, encrypted_data, self.key)
            if found_entry:
                self.output_text.delete(1.0, tk.END)
                self.output_text.insert(tk.END, "Credentials found:\n")
                self.output_text.insert(tk.END, found_entry + "\n")
            else:
                self.output_text.insert(tk.END, "No matching entry found.\n")

    def create_entry(self):
        website_name = self.show_popup("Search Existing Entry", "Enter website name:")
        if website_name:
            username = self.show_popup("Create New Entry", "Enter username:")
            if username:
                password = self.show_popup("Create New Entry", "Enter password:")
                if password:
                    new_entry = f"Website: {website_name}\nUsername: {username}\nPassword: {password}\n\n"
                    encrypted_data = self.read_from_file("encrypted_data.txt")
                    encrypted_entry = self.encrypt_message(new_entry, self.key)
                    encrypted_data += encrypted_entry
                    self.save_to_file(encrypted_data, "encrypted_data.txt")
                    self.output_text.delete(1.0, tk.END)
                    self.output_text.insert(tk.END, "New entry created and saved successfully.\n")

    def show_popup(self, title, message):
        return simpledialog.askstring(title, message)

    def encrypt_message(self, message, key):
        cipher_suite = Fernet(key)
        encrypted_message = cipher_suite.encrypt(message.encode())
        return encrypted_message

    def decrypt_message(self, encrypted_message, key):
        cipher_suite = Fernet(key)
        decrypted_message = cipher_suite.decrypt(encrypted_message).decode()
        return decrypted_message

    def save_to_file(self, data, filename):
        with open(filename, 'wb') as file:
            file.write(data)

    def read_from_file(self, filename):
        try:
            with open(filename, 'rb') as file:
                data = file.read()
            return data
        except FileNotFoundError:
            return b''

    def search_credentials(self, website, encrypted_data, key):
        decrypted_data = self.decrypt_message(encrypted_data, key)
        entries = decrypted_data.split('\n\n')
        for entry in entries:
            if entry.startswith('Website: ' + website):
                return entry
        return None

def main():
    root = tk.Tk()
    root.geometry("400x300")
    app = PasswordManagerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
