from django.core.exceptions import ValidationError
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.validators import EmailValidator, RegexValidator

VERIFIED_DOMAINS = {"gmail", "email", "icloud", "yopmail", "yahoo"}
phone_regex = RegexValidator(
        regex=r"^\+[1-9]\d{1,14}$",
        message="Enter a valid WhatsApp number in international format (e.g. +2348012345678, +14155552671, +919876543210)",
    )


def validate_email_address(value):
    """
    Validates that the email address:
    - Contains '@' and '.' after '@'
    - Has no spaces
    - Ends with '.com'
    - Has domain part in verified domains list
    """
    validator = EmailValidator()
    try:
        validator(value)
    except DjangoValidationError:
        raise ValidationError("Invalid email address format.")

    if " " in value:
        raise ValidationError("Email address cannot contain spaces.")

    if not value.endswith(".com"):
        raise ValidationError("Email address must end with '.com'.")

    try:
        local_part, domain_part = value.split("@")
    except ValueError:
        raise ValidationError("Invalid email address format.")

    domain_name = domain_part.split(".")[0].lower()
    if domain_name not in VERIFIED_DOMAINS:
        raise ValidationError(
            "Email domain must be one of: gmail, email, icloud."
        )