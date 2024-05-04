from django.urls import path
from .views import rate_haiku

urlpatterns = [
    path('rate-haiku/', rate_haiku, name='rate_haiku'),
]
