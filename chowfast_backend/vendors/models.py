from django.db import models
from users.models import User


class Vendor(models.Model):
    vendor_id = models.CharField(
        max_length=15, unique=True, editable=False, null=True, blank=True
    )
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

    def save(self, *args, **kwargs):
        # Save once to get the primary key
        is_new = self.pk is None
        super().save(*args, **kwargs)

        # Generate vendor_id if it's a new record
        if is_new and not self.vendor_id:
            self.vendor_id = f"VEND_{str(self.pk).zfill(4)}"
            Vendor.objects.filter(pk=self.pk).update(vendor_id=self.vendor_id)

    def __str__(self):
        return f"{self.vendor_id or 'Pending ID'} - {self.business_name}"
    
    @property
    def phone_number(self):
        if self.user.phone_number:
            return self.user.phone_number
        return None
