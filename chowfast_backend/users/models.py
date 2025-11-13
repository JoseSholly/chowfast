import uuid

from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from .managers import CustomUserManager, OTPManager, SessionTokenManager
from .mixins import TimestampMixin

PURPOSE_CHOICES = (
    ("email_verification", "Email Verification"),
    ("password_reset", "Password Reset"),
    ("2fa", "Two-Factor Authentication"),
)
class User(AbstractUser):
    USER_TYPES = [
        ("vendor", "Vendor"),
        ("admin", "Admin"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = None  
    email = models.EmailField(unique=True, max_length=255, db_index=True)
    phone_number = models.CharField(max_length=20, unique=True, db_index=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default="vendor")

    is_active = models.BooleanField(default=True)
    is_activated = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone_number"]

    objects = CustomUserManager()

    class Meta:
        db_table = "users"
        ordering = ["-date_joined"]
        constraints = [
            # Explicitly ensures the 'email' field is unique
            models.UniqueConstraint(fields=['email'], name='unique_email_constraint'), 
            
            # Explicitly ensures the 'phone_number' field is unique
            models.UniqueConstraint(fields=['phone_number'], name='unique_phone_number_constraint')
        ]

    def __str__(self):
        return f"{self.email} ({self.user_type})"


class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="otps")
    code = models.CharField(max_length=128)  # store hashed OTP
    purpose = models.CharField(max_length=50, choices=PURPOSE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = OTPManager()

    class Meta:
        indexes = [
            models.Index(fields=["user", "purpose"]),
        ]
        verbose_name = "OTP"

    def is_expired(self, validity_minutes=10):
        return timezone.now() > self.created_at + timezone.timedelta(
            minutes=validity_minutes
        )

    def verify_otp(self, raw_code):
        """
        Verify OTP by checking hashed code.
        """
        return check_password(raw_code, self.code)

    def __str__(self):
        return f"OTP for {self.user.email} ({self.purpose})"


class SessionToken(TimestampMixin, models.Model):
    """
    Stores a temporary session token that authorizes user.
    This token is single-use and time-limited.
    """

    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid1, editable=False, unique=True)
    purpose = models.CharField(max_length=50, choices=PURPOSE_CHOICES)
    expires_at = models.DateTimeField(default=None)
    is_used = models.BooleanField(default=False)

    objects = SessionTokenManager()

    def is_valid(self):
        """Checks if the session token is still valid (not expired and not yet used)."""
        return not self.is_used and self.expires_at > timezone.now()

    def is_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return f"Session for {self.user.email} - {str(self.token)[:10]}..."
