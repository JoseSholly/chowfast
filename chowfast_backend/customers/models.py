from django.db import models


class Customer(models.Model):
    customer_id = models.CharField(max_length=15, unique=True, editable=False, null=True, blank=True, db_index=True)
    phone_number = models.CharField(max_length=20, unique=True, db_index=True, default="")
    location = models.CharField(max_length=100, null=True, blank=True)
    delivery_address = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "customers"
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new and not self.customer_id:
            self.customer_id = f"CUST-{str(self.pk).zfill(5)}"
            Customer.objects.filter(pk=self.pk).update(customer_id=self.customer_id)

    def __str__(self):
        return f"{self.customer_id or 'Pending ID'} - {self.phone_number}"
