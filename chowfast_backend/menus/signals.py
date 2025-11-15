import logging

from cloudinary.uploader import destroy, upload
from decouple import config
from django.db import transaction
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from .models import MenuItem

logger = logging.getLogger(__name__)


FOLDER_NAME = "ChowFast_menu_images"

@receiver(pre_save, sender=MenuItem)
def handle_recipe_image_upload(sender, instance, **kwargs):
    """
    Handles image management with proper error handling:
    - New uploads go to ChowFast_menu_images
    - Recipe renames move to ChowFast_menu_images
    - Image deletions are atomic
    """
    # if not instance.pk:  # New instance
    #     if (
    #         hasattr(instance, "image")
    #         and instance.image
    #         and hasattr(instance.image, "file")
    #     ):
    #         handle_new_upload(instance)
    #         print("New Upload")
    #     return
        

    try:
        old_instance = MenuItem.objects.get(pk=instance.pk)
    except MenuItem.DoesNotExist:
        logger.error(f"MenuItem instance {instance.pk} found in pre_save but not in DB.")
        return

    # Case 1: Image was cleared
    if not instance.image and old_instance.image:
        with transaction.atomic():
            destroy(old_instance.image.public_id)
        return

    # Case 2: Recipe name changed with same image file
    if (
        instance.name != old_instance.name
        and instance.image
        and old_instance.image
        and str(instance.image) == str(old_instance.image)
    ):
        with transaction.atomic():
            try:
                old_public_id = old_instance.image.public_id
                new_public_id = slugify(f"{instance.vendor.vendor_id}_{instance.name}")

                # 1. First upload to new location
                upload(
                    instance.image.url,
                    public_id=new_public_id,
                    folder=FOLDER_NAME,
                    overwrite=True,
                    resource_type="image",
                    invalidate=True,
                )
                

                # 2. Then delete old version
                destroy(old_public_id)

                # 3. Finally update instance
                instance.image = f"{FOLDER_NAME}/{new_public_id}"
                print("Name Changed: Update upload")

            except Exception as e:
                # Ensure we don't leave the instance in an inconsistent state
                instance.image = old_instance.image
                raise RuntimeError(f"Failed to rename image: {str(e)}") from e

    # Case 3: New image uploaded
    elif hasattr(instance.image, "file"):
        with transaction.atomic():
            if old_instance.image:
                destroy(old_instance.image.public_id)
                print("New Image Upload")
            return handle_new_upload(instance)


def handle_new_upload(instance):
    """Handles new uploads with transaction safety"""
    NEW_PUBLIC_ID = slugify(f"{instance.vendor.vendor_id}_{instance.name}")
    try:
        result = upload(
            instance.image.file,
            folder=FOLDER_NAME,
            public_id=NEW_PUBLIC_ID,
            resource_type="image",
            overwrite=True,
            invalidate=True,
        )
        instance.image = result["public_id"]
    except Exception as e:
        raise RuntimeError(f"Image upload failed: {str(e)}") from e


@receiver(post_delete, sender=MenuItem)
def delete_recipe_image(sender, instance, **kwargs):
    """Ensures image deletion when recipe is deleted, only in production"""
    # Check if the environment is production
    is_allowed_to_delete = config('ALLOW_CLOUDINARY_DELETE', default=False, cast=bool)

    if hasattr(instance, "image") and instance.image and is_allowed_to_delete:
        try:
            destroy(instance.image.public_id)
        except Exception as e:
            raise RuntimeError(f"Image deletion failed: {str(e)}") from e
