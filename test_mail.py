import os
import smtplib
from email.message import EmailMessage

# Same environment variables as camera.py
sender = os.environ["ALERT_EMAIL_SENDER"]
receiver = os.environ["ALERT_EMAIL_RECEIVER"]
app_password = os.environ["ALERT_EMAIL_APP_PASSWORD"]

msg = EmailMessage()
msg.set_content("Test mail")
msg["Subject"] = "Test"
msg["From"] = sender
msg["To"] = receiver

server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
server.login(sender, app_password)
server.send_message(msg)
server.quit()

print("Mail sent")
