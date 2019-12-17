from django.urls import path
from rooms import views as room_views

app_name = "core"  # same with namespace in config -> urls.py

urlpatterns = [path("", room_views.HomeView.as_view(), name="home")]