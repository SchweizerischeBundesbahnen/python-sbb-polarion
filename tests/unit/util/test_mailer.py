"""Unit tests for email utilities."""

import unittest
from email.mime.multipart import MIMEMultipart
from smtplib import SMTPException
from unittest.mock import Mock, patch

from python_sbb_polarion.util.mailer import Mailer, MailerError


class TestMailerError(unittest.TestCase):
    """Test MailerError exception class."""

    def test_mailer_error_creation(self) -> None:
        """Test creating MailerError exception."""
        error_msg: str = "Test error message"
        error = MailerError(error_msg)

        self.assertIsInstance(error, Exception)
        self.assertEqual(str(error), error_msg)

    def test_mailer_error_raise(self) -> None:
        """Test raising MailerError exception."""
        with self.assertRaises(MailerError) as context:
            raise MailerError("Custom error")

        self.assertEqual(str(context.exception), "Custom error")


class TestMailer(unittest.TestCase):
    """Test Mailer class."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.smtp_host = "smtp.example.com"
        self.smtp_port = 587
        self.smtp_user = "user@example.com"
        self.smtp_password = "password123"

    def test_init_with_defaults(self) -> None:
        """Test initialization with default parameters."""
        mailer = Mailer()

        self.assertEqual(mailer.smtp_host, "smtp.example.com")
        self.assertEqual(mailer.smtp_port, 587)
        self.assertEqual(mailer.smtp_user, "")
        self.assertEqual(mailer.smtp_password, "")

    def test_init_with_custom_params(self) -> None:
        """Test initialization with custom parameters."""
        mailer = Mailer(smtp_host=self.smtp_host, smtp_port=self.smtp_port, smtp_user=self.smtp_user, smtp_password=self.smtp_password)

        self.assertEqual(mailer.smtp_host, self.smtp_host)
        self.assertEqual(mailer.smtp_port, self.smtp_port)
        self.assertEqual(mailer.smtp_user, self.smtp_user)
        self.assertEqual(mailer.smtp_password, self.smtp_password)

    def test_init_with_partial_params(self) -> None:
        """Test initialization with partial custom parameters."""
        mailer = Mailer(smtp_host="custom.smtp.com", smtp_port=25)

        self.assertEqual(mailer.smtp_host, "custom.smtp.com")
        self.assertEqual(mailer.smtp_port, 25)
        self.assertEqual(mailer.smtp_user, "")
        self.assertEqual(mailer.smtp_password, "")

    @patch("python_sbb_polarion.util.mailer.SMTP")
    @patch("python_sbb_polarion.util.mailer.create_default_context")
    def test_send_message_basic(self, mock_create_context: Mock, mock_smtp: Mock) -> None:
        """Test sending basic email message."""
        mock_server = Mock()
        mock_smtp.return_value.__enter__.return_value = mock_server
        mock_context = Mock()
        mock_create_context.return_value = mock_context

        mailer = Mailer(smtp_host=self.smtp_host, smtp_port=self.smtp_port, smtp_user=self.smtp_user, smtp_password=self.smtp_password)
        mailer.send_message(from_addr="sender@example.com", to_addr=["recipient@example.com"], subject="Test Subject", message="Test message body")

        # Verify SMTP connection was created
        mock_smtp.assert_called_once_with(host=self.smtp_host, port=self.smtp_port)
        # Verify STARTTLS was called (port 587)
        mock_server.starttls.assert_called_once_with(context=mock_context)
        # Verify login was called
        mock_server.login.assert_called_once_with(self.smtp_user, self.smtp_password)
        # Verify send_message was called
        mock_server.send_message.assert_called_once()

    @patch("python_sbb_polarion.util.mailer.SMTP")
    @patch("python_sbb_polarion.util.mailer.create_default_context")
    def test_send_message_without_starttls(self, mock_create_context: Mock, mock_smtp: Mock) -> None:
        """Test sending email without STARTTLS (non-587 port)."""
        mock_server = Mock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        mailer = Mailer(smtp_host=self.smtp_host, smtp_port=25, smtp_user=self.smtp_user, smtp_password=self.smtp_password)
        mailer.send_message(from_addr="sender@example.com", to_addr=["recipient@example.com"], subject="Test", message="Test")

        # Verify STARTTLS was NOT called (port != 587)
        mock_server.starttls.assert_not_called()
        # Verify login and send_message were still called
        mock_server.login.assert_called_once()
        mock_server.send_message.assert_called_once()

    @patch("python_sbb_polarion.util.mailer.SMTP")
    @patch("python_sbb_polarion.util.mailer.create_default_context")
    def test_send_message_with_cc(self, mock_create_context: Mock, mock_smtp: Mock) -> None:
        """Test sending email with CC recipients."""
        mock_server = Mock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        mailer = Mailer(smtp_host=self.smtp_host, smtp_port=self.smtp_port, smtp_user=self.smtp_user, smtp_password=self.smtp_password)
        mailer.send_message(from_addr="sender@example.com", to_addr=["recipient@example.com"], cc_addr=["cc1@example.com", "cc2@example.com"], subject="Test", message="Test")

        # Verify send_message was called
        mock_server.send_message.assert_called_once()
        # Get the MIMEMultipart message that was sent
        sent_message: MIMEMultipart = mock_server.send_message.call_args[0][0]
        self.assertIn("Cc", sent_message)
        self.assertEqual(sent_message["Cc"], "cc1@example.com, cc2@example.com")

    @patch("python_sbb_polarion.util.mailer.SMTP")
    @patch("python_sbb_polarion.util.mailer.create_default_context")
    def test_send_message_with_html(self, mock_create_context: Mock, mock_smtp: Mock) -> None:
        """Test sending email with HTML content."""
        mock_server = Mock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        mailer = Mailer(smtp_host=self.smtp_host, smtp_port=self.smtp_port, smtp_user=self.smtp_user, smtp_password=self.smtp_password)
        html_content: str = "<html><body><h1>Test</h1></body></html>"
        mailer.send_message(from_addr="sender@example.com", to_addr=["recipient@example.com"], subject="Test", message="Plain text", html_message=html_content)

        # Verify send_message was called
        mock_server.send_message.assert_called_once()

    @patch("python_sbb_polarion.util.mailer.SMTP")
    @patch("python_sbb_polarion.util.mailer.create_default_context")
    @patch("python_sbb_polarion.util.mailer.pathlib.Path.read_bytes", return_value=b"file content")
    def test_send_message_with_attachments(self, mock_read_bytes: Mock, mock_create_context: Mock, mock_smtp: Mock) -> None:
        """Test sending email with file attachments."""
        mock_server = Mock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        mailer = Mailer(smtp_host=self.smtp_host, smtp_port=self.smtp_port, smtp_user=self.smtp_user, smtp_password=self.smtp_password)
        mailer.send_message(from_addr="sender@example.com", to_addr=["recipient@example.com"], subject="Test", message="Test", attachments=["/path/to/file.txt"])

        # Verify read_bytes was called once for the attachment
        mock_read_bytes.assert_called_once()
        # Verify send_message was called
        mock_server.send_message.assert_called_once()

    @patch("python_sbb_polarion.util.mailer.SMTP")
    @patch("python_sbb_polarion.util.mailer.create_default_context")
    @patch("python_sbb_polarion.util.mailer.pathlib.Path.read_bytes", return_value=b"file1")
    def test_send_message_with_multiple_attachments(self, mock_read_bytes: Mock, mock_create_context: Mock, mock_smtp: Mock) -> None:
        """Test sending email with multiple attachments."""
        mock_server = Mock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        mailer = Mailer(smtp_host=self.smtp_host, smtp_port=self.smtp_port, smtp_user=self.smtp_user, smtp_password=self.smtp_password)
        mailer.send_message(
            from_addr="sender@example.com",
            to_addr=["recipient@example.com"],
            subject="Test",
            message="Test",
            attachments=["/path/to/file1.txt", "/path/to/file2.pdf"],
        )

        # Verify read_bytes was called twice (once per attachment)
        self.assertEqual(mock_read_bytes.call_count, 2)
        # Verify send_message was called
        mock_server.send_message.assert_called_once()

    @patch("python_sbb_polarion.util.mailer.SMTP")
    def test_send_message_smtp_error(self, mock_smtp: Mock) -> None:
        """Test handling of SMTP errors."""
        mock_server = Mock()
        mock_smtp.return_value.__enter__.return_value = mock_server
        mock_server.send_message.side_effect = SMTPException("SMTP error occurred")

        mailer = Mailer(smtp_host=self.smtp_host, smtp_port=self.smtp_port, smtp_user=self.smtp_user, smtp_password=self.smtp_password)

        with self.assertRaises(MailerError) as context:
            mailer.send_message(from_addr="sender@example.com", to_addr=["recipient@example.com"], subject="Test", message="Test")

        self.assertIn("SMTP error occurred", str(context.exception))

    @patch("python_sbb_polarion.util.mailer.SMTP")
    def test_send_message_generic_error(self, mock_smtp: Mock) -> None:
        """Test handling of generic errors."""
        mock_server = Mock()
        mock_smtp.return_value.__enter__.return_value = mock_server
        mock_server.send_message.side_effect = Exception("Generic error")

        mailer = Mailer(smtp_host=self.smtp_host, smtp_port=self.smtp_port, smtp_user=self.smtp_user, smtp_password=self.smtp_password)

        with self.assertRaises(MailerError) as context:
            mailer.send_message(from_addr="sender@example.com", to_addr=["recipient@example.com"], subject="Test", message="Test")

        self.assertIn("An error occurred", str(context.exception))

    @patch("python_sbb_polarion.util.mailer.SMTP")
    @patch("python_sbb_polarion.util.mailer.create_default_context")
    def test_send_message_multiple_recipients(self, mock_create_context: Mock, mock_smtp: Mock) -> None:
        """Test sending email to multiple recipients."""
        mock_server = Mock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        mailer = Mailer(smtp_host=self.smtp_host, smtp_port=self.smtp_port, smtp_user=self.smtp_user, smtp_password=self.smtp_password)
        to_addresses: list[str] = ["recipient1@example.com", "recipient2@example.com", "recipient3@example.com"]
        mailer.send_message(from_addr="sender@example.com", to_addr=to_addresses, subject="Test", message="Test")

        # Verify send_message was called
        mock_server.send_message.assert_called_once()
        # Get the message that was sent
        sent_message: MIMEMultipart = mock_server.send_message.call_args[0][0]
        self.assertEqual(sent_message["To"], "recipient1@example.com, recipient2@example.com, recipient3@example.com")

    @patch("python_sbb_polarion.util.mailer.SMTP")
    @patch("python_sbb_polarion.util.mailer.create_default_context")
    @patch("python_sbb_polarion.util.mailer.logger")
    def test_send_message_logs_success(self, mock_logger: Mock, mock_create_context: Mock, mock_smtp: Mock) -> None:
        """Test that successful send is logged."""
        mock_server = Mock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        mailer = Mailer(smtp_host=self.smtp_host, smtp_port=self.smtp_port, smtp_user=self.smtp_user, smtp_password=self.smtp_password)
        to_addresses: list[str] = ["recipient@example.com"]
        mailer.send_message(from_addr="sender@example.com", to_addr=to_addresses, subject="Test", message="Test")

        # Verify success was logged with lazy formatting
        mock_logger.info.assert_called_once_with("Email sent successfully to %s", to_addresses)

    @patch("python_sbb_polarion.util.mailer.SMTP")
    @patch("python_sbb_polarion.util.mailer.create_default_context")
    def test_message_structure(self, mock_create_context: Mock, mock_smtp: Mock) -> None:
        """Test that message structure is correct."""
        mock_server = Mock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        mailer = Mailer(smtp_host=self.smtp_host, smtp_port=self.smtp_port, smtp_user=self.smtp_user, smtp_password=self.smtp_password)
        mailer.send_message(from_addr="sender@example.com", to_addr=["recipient@example.com"], subject="Test Subject", message="Test message body")

        # Get the message that was sent
        sent_message: MIMEMultipart = mock_server.send_message.call_args[0][0]

        # Verify message structure
        self.assertIsInstance(sent_message, MIMEMultipart)
        self.assertEqual(sent_message["From"], "sender@example.com")
        self.assertEqual(sent_message["To"], "recipient@example.com")
        self.assertEqual(sent_message["Subject"], "Test Subject")


if __name__ == "__main__":
    unittest.main()
