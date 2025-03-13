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

from drf_spectacular.utils import (
    extend_schema, OpenApiExample, OpenApiParameter,
    OpenApiResponse
)
from .serializers import (
    CustomTokenObtainPairSerializer,
    CreateUserSerializer
)

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

