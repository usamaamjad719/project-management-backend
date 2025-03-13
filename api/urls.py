from django.urls import path
from . import views


urlpatterns = [
    path('token/', views.CustomTokenObtainPairView.as_view()),
    path('register/', views.RegisterView.as_view()),

    path('projects/', views.ProjectListCreateAPIView.as_view()),
    path('projects/<str:id>/', views.ProjectRetrieveUpdateDestroyAPIView.as_view()),
]

