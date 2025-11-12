from django.db import models
from users.models import User


class Vendor(models.Model):
    user = models.OneToOneField(User, related_name="vendor", on_delete=models.CASCADE)
    business_name = models.CharField(max_length=200)
    address = models.TextField(blank=True, null=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    total_orders = models.PositiveIntegerField(default=0)
    online = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "vendors"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.business_name} ({self.user.email})"
