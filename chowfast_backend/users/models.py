import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from .manager import CustomUserManager


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
