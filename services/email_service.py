import os

class EmailService:
    def __init__(self, smtp_host: str | None = None):
        self.smtp_host = smtp_host or os.getenv("SMTP_HOST")

    def send_email(self, to: str, subject: str, body: str) -> bool:
        # Placeholder - print to logs instead of sending
        print(f"Sending email to {to}: {subject}\n{body}\n")
        return True
