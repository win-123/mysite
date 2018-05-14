from django.urls import path
from . import views



urlpatterns = [

    path("approve_change/", views.approve_change, name="approve_change"),
    
]