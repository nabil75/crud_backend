import smtplib
from email.message import EmailMessage

def send_test_email():
    msg = EmailMessage()
    msg.set_content("This is a test email sent using aiosmtpd.")

    msg['Subject'] = "Test Email"
    msg['From'] = "sender@example.com"
    msg['To'] = "receiver@example.com"

    # Connect to the SMTP server running on localhost:8025
    with smtplib.SMTP('localhost', 8025) as server:
        server.send_message(msg)

send_test_email()