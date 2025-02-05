import asyncio
import os
from email.message import EmailMessage
from aiosmtpd.controller import Controller
from datetime import datetime


class EmailHandler:
    def __init__(self, storage_dir="emails"):
        # Create a directory to store emails if it doesn't exist
        os.makedirs(storage_dir, exist_ok=True)
        self.storage_dir = storage_dir

    async def handle_DATA(self, server, session, envelope):
        # Handle the incoming email data
        mail_from = envelope.mail_from
        rcpt_tos = envelope.rcpt_tos
        message_data = envelope.content.decode('utf-8', errors='replace')

        # Create a filename based on the current timestamp
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = os.path.join(self.storage_dir, f"email_{timestamp}.txt")

        # Store the email in the directory
        with open(filename, 'w') as f:
            f.write(f"From: {mail_from}\n")
            f.write(f"To: {', '.join(rcpt_tos)}\n")
            f.write(f"Data:\n{message_data}\n")

        print(f"Email saved to {filename}")

        # Log the email to the console
        print(f"Received message from {mail_from}")
        print(f"Message sent to {rcpt_tos}")
        print(f"Message data:\n{message_data}")

        return '250 OK'


async def start_smtp_server():
    # Create an instance of EmailHandler to process incoming emails
    handler = EmailHandler()

    # Create and start the SMTP server
    controller = Controller(handler, hostname='localhost', port=8025)
    controller.start()

    print("SMTP server running on localhost:8025")
    try:
        while True:
            await asyncio.sleep(3600)  # Keep the server running
    except KeyboardInterrupt:
        print("Stopping SMTP server...")
        controller.stop()


# Run the server
if __name__ == "__main__":
    asyncio.run(start_smtp_server())