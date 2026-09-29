import smtplib
from email.message import EmailMessage


# Email Alert System

def send_email_alert(subject, message, receiver_email):

    print("Email Alert")
    print("----------------")
    print("Subject:", subject)
    print("Message:", message)
    print("Receiver:", receiver_email)

    # Create email
    email = EmailMessage()

    email["Subject"] = subject
    email["From"] = "YOUR_EMAIL"
    email["To"] = receiver_email

    email.set_content(message)