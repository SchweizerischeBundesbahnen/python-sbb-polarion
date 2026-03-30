"""Email sending utilities."""

import logging
import pathlib
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP, SMTPException
from ssl import create_default_context


logger = logging.getLogger(__name__)


class MailerError(Exception):
    """Custom exception class for Mailer errors."""


class Mailer:
    """The Mailer class is a helper utility for sending emails."""

    def __init__(self, smtp_host: str = "smtp.example.com", smtp_port: int = 587, smtp_user: str = "", smtp_password: str = "") -> None:
        """Initialize Mailer with SMTP configuration.

        Args:
            smtp_host: SMTP server hostname (default: smtp.example.com)
            smtp_port: SMTP server port (default: 587 for STARTTLS)
            smtp_user: SMTP authentication username
            smtp_password: SMTP authentication password
        """
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password

    def send_message(
        self,
        from_addr: str,
        to_addr: list[str],
        subject: str,
        message: str,
        cc_addr: list[str] | None = None,
        html_message: str | None = None,
        attachments: list[str] | None = None,
    ) -> None:
        """Sends an email with the given arguments.

        Args:
            from_addr: Sender email address
            to_addr: List of recipient email addresses
            subject: Email subject
            message: Plain text message body
            cc_addr: Optional list of CC email addresses
            html_message: Optional HTML message body
            attachments: Optional list of file paths to attach

        Raises:
            MailerError: If SMTP error or other error occurs during sending
        """
        msg = MIMEMultipart()
        msg["From"] = from_addr
        msg["To"] = ", ".join(to_addr)
        msg["Subject"] = subject

        if cc_addr:
            msg["Cc"] = ", ".join(cc_addr)

        msg.attach(MIMEText(message, "plain"))
        if html_message:
            msg.attach(MIMEText(html_message, "html"))

        if attachments:
            for filename in attachments:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(pathlib.Path(filename).read_bytes())
                encoders.encode_base64(part)
                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename={pathlib.Path(filename).name}",
                )
                msg.attach(part)

        ctx: ssl.SSLContext = create_default_context()

        try:
            with SMTP(host=self.smtp_host, port=self.smtp_port) as server:
                if self.smtp_port == 587:
                    server.starttls(context=ctx)
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
                logger.info("Email sent successfully to %s", to_addr)
        except SMTPException as e:
            raise MailerError(f"SMTP error occurred: {e}") from e
        except Exception as e:
            raise MailerError(f"An error occurred: {e}") from e
