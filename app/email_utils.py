import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

load_dotenv()

MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_FROM = os.getenv("MAIL_FROM")
MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")


def send_verification_email(to_email: str, username: str, token: str):
    verification_link = f"{BASE_URL}/auth/verify?token={token}"

    message = MIMEMultipart("alternative")
    message["Subject"] = "Verify your Task account"
    message["From"] = MAIL_FROM
    message["To"] = to_email

    html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: auto; padding: 20px;">
        <h2>Welcome to Task, {username}!</h2>
        <p>Thanks for registering. Please verify your email address to activate your account.</p>
        <a href="{verification_link}"
            style="display: inline-block; padding: 12px 24px; background-color: #4F46E5;
                color: white; text-decoration: none; border-radius: 6px; margin: 20px 0;">
        Verify Email
        </a>
        <p>Or copy this link into your browser:</p>
        <p style="color: #6B7280; word-break: break-all;">{verification_link}</p>
        <p style="color: #9CA3AF; font-size: 12px;">This link expires in 24 hours. If you didn't register, ignore this email.</p>
    </body>
    </html>
    """

    message.attach(MIMEText(html, "html"))

    with smtplib.SMTP(MAIL_SERVER, MAIL_PORT) as server:
        server.ehlo()
        server.starttls()
        server.login(MAIL_USERNAME, MAIL_PASSWORD)
        server.sendmail(MAIL_FROM, to_email, message.as_string())
