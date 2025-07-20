from django.http import HttpResponse
from django_ratelimit.decorators import ratelimit
from ratelimit.decorators import ratelimit


#def home(request):
   # return HttpResponse("Welcome to ALX Backend Security IP Tracking!")

from django.http import HttpResponse
from ratelimit.decorators import ratelimit
from django.contrib.auth.decorators import login_required

# Rate limit key function by IP address
def get_ip(request):
    return request.META.get('REMOTE_ADDR')

# Anonymous user rate limit: 5 req/min
@ratelimit(key='ip', rate='5/m', block=True)
def anonymous_view(request):
    return HttpResponse("Anonymous user: Access granted.")

# Authenticated user rate limit: 10 req/min
@ratelimit(key='ip', rate='10/m', block=True)
@login_required
def authenticated_view(request):
    return HttpResponse("Authenticated user: Access granted.")