import smtplib
from email.message import EmailMessage

def send_email(subject, body, to_email):
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['To'] = to_email
    msg['From'] = "ksdrohit28@gmail.com"  # <-- Tera email

    password = "bssawnzuocecrifi"  # <-- Tera 16-digit app password (safe here)

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login("ksdrohit28@gmail.com", password)  # <-- Tera email & app password
        smtp.send_message(msg)