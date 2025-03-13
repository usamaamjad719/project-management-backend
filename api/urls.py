from django.urls import path
from . import views


urlpatterns = [
    path('token/', views.CustomTokenObtainPairView.as_view()),
    path('register/', views.RegisterView.as_view()),
]

