from django.urls import path
from .views import profile

app_name = 'myaccount'
urlpatterns = [
    path('profile/', profile, name="profile"),
]