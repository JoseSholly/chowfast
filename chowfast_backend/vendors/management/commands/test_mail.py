from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Send a simple test email via Mailgun to verify setup"

    def add_arguments(self, parser):
        parser.add_argument(
            '--to',
            type=str,
            help='Email address to send the test email to',
            required=True,  # Force user to provide it
        )

    def handle(self, *args, **options):
        recipient = options['to']

        self.stdout.write(f"Sending test email to: {recipient}")

        send_mail(
            subject="Test Email – Mailgun Works!",
            message="Hello! If you see this, your Django + Mailgun email setup is working perfectly.",
            from_email=settings.DEFAULT_FROM_EMAIL,  # Uses DEFAULT_FROM_EMAIL
            recipient_list=[recipient],
            fail_silently=False,
        )

        self.stdout.write(self.style.SUCCESS("Test email sent!"))


# python manage.py test_mail --to you@example.com