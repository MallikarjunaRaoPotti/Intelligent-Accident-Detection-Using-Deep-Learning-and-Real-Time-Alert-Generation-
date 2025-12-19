import smtplib
from email.message import EmailMessage

msg = EmailMessage()
msg.set_content("Test mail")
msg["Subject"] = "Test"
msg["From"] = "karjuna2004@gmail.com"
msg["To"] = "mallikarjunraopotti@gmail.com"

server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
server.login("karjuna2004@gmail.com", "zftt meyx ckif zddb")
server.send_message(msg)
server.quit()

print("Mail sent")
