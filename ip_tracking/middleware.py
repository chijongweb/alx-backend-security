from ipware import get_client_ip
from .models import RequestLog
from django.utils.timezone import now

class IPTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip, _ = get_client_ip(request)
        if ip:
            RequestLog.objects.create(
                ip_address=ip,
                path=request.path,
                timestamp=now()
            )
        return self.get_response(request)
