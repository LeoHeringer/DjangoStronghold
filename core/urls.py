from django.urls import path
from . import views

urlpatterns = [
    path('api/users/', views.user_list),
    path('api/users/<int:pk>/', views.user_detail),
]
