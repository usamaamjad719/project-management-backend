from django.contrib.auth import get_user_model

from rest_framework import views
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import (
    TokenObtainPairView
)
from rest_framework_simplejwt.tokens import (
    RefreshToken
)
from rest_framework import generics, permissions, filters

from django_filters.rest_framework import DjangoFilterBackend

from drf_spectacular.utils import (
    extend_schema, OpenApiExample, OpenApiParameter,
    OpenApiResponse
)

from .serializers import *
from .models import *
from .custom_apiviews import CustomListCreateAPIView


UserModel = get_user_model()


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Added Userinfo object in response
    """
    serializer_class = CustomTokenObtainPairSerializer
    @extend_schema(
        request={
            'application/json': {
                'email': 'admin@gmail.com',
                'password': 'admin'
            }
        },
        examples=[
            OpenApiExample(
                'Login Example',
                description="Use these default credentials for login.",
                value={
                    'email': 'admin@gmail.com',
                    'password': 'admin'
                },
                request_only=True
            )
        ]
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class RegisterView(views.APIView):
    """
    Register a user
    """
    @extend_schema(
        request={
            'application/json': CreateUserSerializer
        },
        tags=['user']
    )
    def post(self, request, *args, **kwargs):

        # Check if a user with the same email and is_visible=False exists
        existing_user = UserModel.non_visible_objects.filter(email=request.data.get('email')).first()

        if existing_user:
            # If user exists, update their information
            serializer = CreateUserSerializer(existing_user, data=request.data)
        else:
            # If user does not exist, create a new one
            serializer = CreateUserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ProjectListCreateAPIView(CustomListCreateAPIView):
    # permission_classes = [permissions.IsAuthenticated]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    
    search_fields = ['name', 'description', 'created_by', 'created_at', 'updated_at']
    
    ordering_fields = ['name', 'description', 'created_by', 'created_at', 'updated_at']
    
    filterset_fields = {
        'name': ['exact', 'in'],
        'description': ['exact', 'in'],
        'created_by': ['exact', 'in'],
        'created_at': ['exact', 'in'],
        'updated_at': ['exact', 'in'],
    }
    
    def get_queryset(self):
        return Project.visible_objects.all().order_by('-created_at')

    def get_serializer_class(self):
        method = self.request.method

        if method == 'GET':
            return ProjectListSerializer
        elif method == 'POST':
            return ProjectCreateOrUpdateSerializer
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @extend_schema(tags=['Project'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(tags=['Project'])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)



class ProjectRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [permissions.IsAuthenticated]
    queryset = Project.visible_objects.all()
    http_method_names = ['get', 'put', 'delete']
    lookup_url_kwarg = 'id'

    def get_serializer_class(self):
        method = self.request.method

        if method == 'GET':
            return ProjectListSerializer
        elif method == 'PUT':
            return ProjectCreateOrUpdateSerializer
    
    def perform_destroy(self, instance):
        instance.soft_delete()

    @extend_schema(tags=['Project'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(tags=['Project'])
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
    
    @extend_schema(tags=['Project'])
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

