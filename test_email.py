from notifier import send_email

subject = "📈 Stock Price Alert Test"
body = "Hello Bhai,\n\nYeh test email hai to check if your alert system is working. 🔥"
to_email = "ksdrohit28@gmail.com"  # Apna hi email daal test ke liye

send_email(subject, body, to_email)