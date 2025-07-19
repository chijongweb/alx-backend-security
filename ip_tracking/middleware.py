from ipware import get_client_ip
from .models import RequestLog, BlockedIP
from django.utils.timezone import now
import requests
from django.core.cache import cache
from django.http import HttpResponseForbidden

class IPTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip, _ = get_client_ip(request)

        if ip:
            # Blocked IP Check
            if BlockedIP.objects.filter(ip_address=ip).exists():
                return HttpResponseForbidden("Access Denied")

            # Cache Key
            cache_key = f"geo:{ip}"
            geo = cache.get(cache_key)

            if not geo:
                try:
                    res = requests.get(f"https://ipapi.co/{ip}/json/", timeout=3)
                    data = res.json()
                    geo = {
                        "country": data.get("country_name", "Unknown"),
                        "city": data.get("city", "Unknown")
                    }
                    cache.set(cache_key, geo, 60 * 60 * 24)  # Cache for 24 hours
                except Exception:
                    geo = {"country": "Unknown", "city": "Unknown"}

            # Save Log
            RequestLog.objects.create(
                ip_address=ip,
                path=request.path,
                timestamp=now(),
                country=geo.get("country"),
                city=geo.get("city"),
            )

        return self.get_response(request)