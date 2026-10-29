import json
import logging
import urllib.error
import urllib.request
import uuid
from email.utils import parseaddr
from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail.backends.smtp import EmailBackend as DjangoSMTPEmailBackend

logger = logging.getLogger(__name__)


class BrevoAPIEmailBackend(BaseEmailBackend):
    """
    Django EmailBackend that sends transactional emails via Brevo's HTTPS API
    (https://api.brevo.com/v3/smtp/email).

    Works on PythonAnywhere (including Free tier via HTTPS proxy) as well as
    Render and local development, bypassing SMTP port blocks (587/465).

    If BREVO_API_KEY is not configured and EMAIL_HOST_PASSWORD is an SMTP key
    (not starting with 'xkeysib-'), it gracefully falls back to Django's SMTP backend.
    """

    API_URL = "https://api.brevo.com/v3/smtp/email"

    def __init__(self, fail_silently=False, **kwargs):
        super().__init__(fail_silently=fail_silently, **kwargs)
        raw_key = getattr(settings, "BREVO_API_KEY", "").strip()
        if raw_key == "YOUR_BREVO_API_KEY_HERE":
            raw_key = ""
        self.api_key = (
            raw_key
            or (
                getattr(settings, "EMAIL_HOST_PASSWORD", "").strip()
                if getattr(settings, "EMAIL_HOST_PASSWORD", "").strip().startswith("xkeysib-")
                else ""
            )
        )
        self._smtp_fallback_kwargs = kwargs

    def send_messages(self, email_messages):
        if not email_messages:
            return 0

        # If no Brevo HTTP API key is present, fall back to standard SMTP
        if not self.api_key:
            smtp_backend = DjangoSMTPEmailBackend(
                fail_silently=self.fail_silently, **self._smtp_fallback_kwargs
            )
            return smtp_backend.send_messages(email_messages)

        sent_count = 0
        for message in email_messages:
            if self._send_via_brevo_api(message):
                sent_count += 1
        return sent_count

    def _send_via_brevo_api(self, message):
        if not message.to:
            return False

        from_email_raw = message.from_email or getattr(
            settings, "DEFAULT_FROM_EMAIL", "info@nexuscustomerservice.online"
        )
        sender_name, sender_email = parseaddr(from_email_raw)
        if not sender_email:
            sender_email = from_email_raw
        if not sender_name:
            sender_name = getattr(settings, "BREVO_SENDER_NAME", "Nexus Trust Bank")

        # Extract HTML content if attached via EmailMultiAlternatives / send_mail(..., html_message=...)
        html_content = None
        if getattr(message, "content_subtype", "plain") == "html":
            html_content = message.body
        for alt_content, mimetype in getattr(message, "alternatives", []):
            if mimetype == "text/html":
                html_content = alt_content
                break

        payload = {
            "sender": {"name": sender_name, "email": sender_email},
            "to": [{"email": addr} for addr in message.to if addr],
            "subject": message.subject,
            "textContent": message.body or " ",
            "headers": {
                "X-Entity-Ref-ID": str(uuid.uuid4()),
            },
        }
        if html_content:
            payload["htmlContent"] = html_content
        if getattr(message, "cc", None):
            payload["cc"] = [{"email": addr} for addr in message.cc if addr]
        if getattr(message, "bcc", None):
            payload["bcc"] = [{"email": addr} for addr in message.bcc if addr]
        if getattr(message, "reply_to", None):
            reply_addr = message.reply_to[0]
            payload["replyTo"] = {"email": reply_addr}

        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            self.API_URL,
            data=data,
            headers={
                "accept": "application/json",
                "api-key": self.api_key,
                "content-type": "application/json",
                "User-Agent": "NexusTrustBank/1.0",
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(req, timeout=20) as response:
                status_code = response.getcode()
                if 200 <= status_code < 300:
                    return True
                body = response.read().decode("utf-8", errors="replace")
                raise RuntimeError(f"Brevo API returned HTTP {status_code}: {body}")
        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8", errors="replace")
            logger.error(f"Brevo API HTTPError {e.code}: {error_body}")
            if not self.fail_silently:
                raise RuntimeError(f"Brevo API HTTP {e.code}: {error_body}") from e
            return False
        except Exception as e:
            logger.error(f"Brevo API error: {e}")
            if not self.fail_silently:
                raise
            return False
