from django.urls import path
from . import views


urlpatterns = [
    path('token/', views.CustomTokenObtainPairView.as_view()),
    path('register/', views.RegisterView.as_view()),

    # Project
    path('projects/', views.ProjectListCreateAPIView.as_view()),
    path('projects/<str:id>/', views.ProjectRetrieveUpdateDestroyAPIView.as_view()),

    # ProjectRole
    path('project-roles/', views.ProjectRoleListCreateAPIView.as_view()),
    path('project-roles/<str:id>/', views.ProjectRoleRetrieveUpdateDestroyAPIView.as_view()),

    # Comment
    path('comments/', views.CommentListCreateAPIView.as_view()),
    path('comments/<str:id>/', views.CommentRetrieveUpdateDestroyAPIView.as_view()),

]

