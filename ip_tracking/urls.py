from django.urls import path
from .views import anonymous_view, authenticated_view

urlpatterns = [
    path('anon/', anonymous_view, name='anon'),
    path('auth/', authenticated_view, name='auth'),
]
