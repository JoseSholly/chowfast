import logging

from django.utils import timezone

logger = logging.getLogger(__name__)

class LastActiveMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        user = getattr(request, "user", None)
        if user and user.is_authenticated:
            # update once per minute to reduce writes
            if not user.last_active or (timezone.now() - user.last_active).seconds > 60:
                user.__class__.objects.filter(pk=user.pk).update(last_active=timezone.now())
        return response
