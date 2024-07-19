from django import views
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("/create-client", views.create_client, name="create_client"),
]
