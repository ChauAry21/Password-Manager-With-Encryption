from cryptography.fernet import Fernet

# Function to encrypt a message using a key
def encrypt_message(message, key):
    cipher_suite = Fernet(key)
    encrypted_message = cipher_suite.encrypt(message.encode())
    return encrypted_message

# Function to decrypt a message using a key
def decrypt_message(encrypted_message, key):
    cipher_suite = Fernet(key)
    decrypted_message = cipher_suite.decrypt(encrypted_message).decode()
    return decrypted_message

# Function to save encrypted data to a file
def save_to_file(data, filename):
    with open(filename, 'wb') as file:
        file.write(data)

# Function to read encrypted data from a file
def read_from_file(filename):
    with open(filename, 'rb') as file:
        data = file.read()
    return data

# Function to search for credentials in the encrypted data
def search_credentials(website, encrypted_data, key):
    decrypted_data = decrypt_message(encrypted_data, key)
    entries = decrypted_data.split('\n\n')
    for entry in entries:
        if entry.startswith('Website: ' + website):
            return entry
    return None

def main():
    # Generate an encryption key
    key = Fernet.generate_key()

    # Initial message
    print("Welcome to Aryan's password manager!")

    # Command loop
    while True:
        i = input('What would you like to do? (cmds): \n')

        if i == 'cmds':
            print('cmds ---> provides a list of all accepted commands and the accepted syntax\n')
            print('search [website name] ---> searches for pre-existing website credentials entered previously\n')
            print('new [website name], [username], [password] ---> creates a new entry and encrypts it to ensure credential security\n')
            print('exit ---> exit the program')

        elif i.startswith('search ') and len(i.split()) == 2:
            website_name = i.split()[1]
            encrypted_data = read_from_file("encrypted_data.txt")
            found_entry = search_credentials(website_name, encrypted_data, key)
            if found_entry:
                print("Credentials found:")
                print(found_entry)
            else:
                print("No credentials found for " + i.split(' ', 1))

        elif i.startswith('new '):
            # Split the input by spaces
            command_parts = i.split()
            if len(command_parts) >= 4 and command_parts[0] == 'new':
                website = command_parts[1]
                username = command_parts[2]
                password = ' '.join(command_parts[3:])  # Join remaining parts as password
                new_entry = f"Website: {website}\nUsername: {username}\nPassword: {password}\n\n"
                encrypted_data = read_from_file("encrypted_data.txt")
                encrypted_entry = encrypt_message(new_entry, key)
                encrypted_data += encrypted_entry
                save_to_file(encrypted_data, "encrypted_data.txt")
                print("New entry created and saved successfully.")
            else:
                print("Invalid command format. Type 'cmds' to see available commands.")



        elif i == 'exit':
            print("Exiting...")
            break

        else:
            print("Invalid command. Type 'cmds' to see available commands.")

if __name__ == "__main__":
    main()
