import os
from dotenv import load_dotenv
import smtplib
from email.message import EmailMessage


# Load environment variables from .env
load_dotenv()


# Get email settings
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")


# Email Alert System
def send_email_alert(subject, message, receiver_email=None):

    # Use receiver from .env if not provided
    if receiver_email is None:
        receiver_email = EMAIL_RECEIVER

    # Safe test mode
    if (
        not EMAIL_SENDER
        or not EMAIL_PASSWORD
        or EMAIL_PASSWORD == "NOT_SET"
    ):
        print("Email Alert - TEST MODE")
        print("------------------------")
        print("Subject:", subject)
        print("Message:", message)
        print("Receiver:", receiver_email)
        print("Actual email was not sent.")
        return

    # Create email
    email = EmailMessage()

    email["Subject"] = subject
    email["From"] = EMAIL_SENDER
    email["To"] = receiver_email

    email.set_content(message)

    # Send email
    try:

        with smtplib.SMTP("smtp.gmail.com", 587) as server:

            server.starttls()

            server.login(
                EMAIL_SENDER,
                EMAIL_PASSWORD
            )

            server.send_message(email)

        print("Email sent successfully!")

    except Exception as error:

        print("Email sending failed.")
        print("Error:", error)