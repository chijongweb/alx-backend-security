from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import SuspiciousIP
from .middleware import LoggedIP
from django.db.models import Count

SENSITIVE_PATHS = ['/admin', '/login']

@shared_task
def detect_anomalies():
    now = timezone.now()
    one_hour_ago = now - timedelta(hours=1)

    # Flag IPs with >100 requests in past hour
    high_freq_ips = (
        LoggedIP.objects
        .filter(timestamp__gte=one_hour_ago)
        .values('ip_address')
        .annotate(request_count=Count('id'))
        .filter(request_count__gt=100)
    )

    for entry in high_freq_ips:
        ip = entry['ip_address']
        SuspiciousIP.objects.get_or_create(ip_address=ip, reason='High request rate (>100/hour)')

    # Flag IPs accessing sensitive paths
    sensitive_hits = (
        LoggedIP.objects
        .filter(path__in=SENSITIVE_PATHS, timestamp__gte=one_hour_ago)
        .values_list('ip_address', flat=True)
        .distinct()
    )

    for ip in sensitive_hits:
        SuspiciousIP.objects.get_or_create(ip_address=ip, reason='Accessed sensitive path')