import random
from datetime import timedelta

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import BaseUserManager
from django.db import models
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("user_type", "admin")

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class OTPManager(models.Manager):
    def create_otp(self, user, purpose, length=6):
        """
        Creates and stores a hashed OTP for the given user and purpose.
        """
        raw_code = "".join([str(random.randint(0, 9)) for _ in range(length)])  # numeric OTP
        hashed_code = make_password(raw_code)

        otp = self.create(
            user=user,
            code=hashed_code,
            purpose=purpose,
        )
        return otp, raw_code
    

class SessionTokenManager(models.Manager):
    def create_token(self, user, purpose, expiry_hours=12):
        """
        Creates a new session token for the given user and purpose.
        Defaults to 12 hours expiry.
        """
        # Invalidate old tokens for this user & purpose (optional, depending on business rules)
        self.filter(user=user, purpose=purpose, is_used=False).update(is_used=True)

        expires_at = timezone.now() + timedelta(hours=expiry_hours)

        token = self.create(
            user=user,
            purpose=purpose,
            expires_at=expires_at,
        )
        return token