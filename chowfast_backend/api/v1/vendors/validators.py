from django.core.validators import RegexValidator

phone_regex = RegexValidator(
        regex=r"^\+[1-9]\d{1,14}$",
        message="Enter a valid WhatsApp number in international format (e.g. +2348012345678, +14155552671, +919876543210)",
    )
