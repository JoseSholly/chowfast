from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def send_html_email(subject, to_email, template_name, context):
    """
    Send ONLY HTML email (no plain text fallback).
    """

    html_content = render_to_string(template_name, context)

    email = EmailMultiAlternatives(
        subject=subject,
        body=html_content,                     # Set HTML as the main body
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[to_email],
    )
    email.content_subtype = "html"            # This makes the email HTML-only
    email.send(fail_silently=False)



def send_signup_otp_email(user, otp):
    subject = "Your ChowFast Email Verification Code"
    context = {
        "user": user,
        "otp": otp,
    }

    send_html_email(
        subject=subject,
        to_email=user.email,
        template_name="email/signup_otp_email.html", 
        context=context,
    )

