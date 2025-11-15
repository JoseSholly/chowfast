import uuid

from cloudinary.models import CloudinaryField
from django.db import models
from vendors.models import Vendor
from django.utils.text import slugify


class MenuItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vendor = models.ForeignKey(Vendor, related_name="menu_items", on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=50, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    image = CloudinaryField(
        "image", 
        folder="ChowFast_menu_images", 
        public_id=lambda instance: slugify(f"{instance.vendor.vendor_id}_{instance.name}"),
        overwrite=True,
        resource_type='image',
        blank=True, 
        null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "menu_items"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.vendor.business_name}"

    @property
    def image_url(self):
        """Generate full Cloudinary URL for the food image."""
        return self.image.build_url(secure=True) if self.image else None