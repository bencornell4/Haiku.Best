from django.urls import path
from haikujudge import views

urlpatterns = [
    path('haikujudge/', views.haiku_judge),
    path('/', views.haiku_head),
]
