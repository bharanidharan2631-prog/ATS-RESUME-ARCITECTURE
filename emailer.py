import os
import smtplib
from dotenv import load_dotenv
from email.message import EmailMessage

load_dotenv()

def send_email(receiver_email, file_path):

    sender_email = os.getenv("EMAIL_USER")
    sender_password = os.getenv("EMAIL_PASS")

    if not sender_email:
        raise Exception("EMAIL_USER not found in .env")

    if not sender_password:
        raise Exception("EMAIL_PASS not found in .env")

    msg = EmailMessage()

    msg["Subject"] = "ATS Optimized Resume"
    msg["From"] = sender_email
    msg["To"] = receiver_email

    msg.set_content(
        "Hello,\n\nYour ATS Optimized Resume is attached.\n\nRegards,\nATS Resume Analyzer"
    )

    with open(file_path, "rb") as f:
        file_data = f.read()

    msg.add_attachment(
        file_data,
        maintype="application",
        subtype="pdf",
        filename="ATS_Resume.pdf"
    )

    print("Connecting Gmail...")

    with smtplib.SMTP("smtp.gmail.com", 587, timeout=15) as server:

        server.starttls()

        print("Logging in...")

        server.login(
            sender_email,
            sender_password
        )

        print("Sending Email...")

        server.send_message(msg)

        print("Email Sent Successfully")