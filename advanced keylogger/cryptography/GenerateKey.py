from cryptography.fernet import Fernet

try:
    # Generate a key
    key = Fernet.generate_key()

    # Specify the full path to the file
    file_path = r"D:\vscode\python\advanced_keylogger\cryptography\encryption_key.txt" # edit this  

    # Open a file in binary write mode
    with open(file_path, "wb") as file:
        # Write the key to the file after encoding it
        file.write(key)
    print("Encryption key saved successfully.")

except Exception as e:
    print("An error occurred while creating the encryption key file:", str(e))
