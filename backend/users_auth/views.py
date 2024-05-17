from django.contrib.auth import get_user_model
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from . import serializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken



User = get_user_model()

class UserRegisterationAPIView(GenericAPIView):
    
    permission_classes = (AllowAny,)
    serializer_class = serializers.UserRegisterationSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = RefreshToken.for_user(user)
        data = serializer.data
        data["tokens"] = {
            "refresh": str(token),
            "access": str(token.access_token)
        }
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class UserLoginAPIView(GenericAPIView):
    
    permission_classes = (AllowAny,)
    serializer_class = serializers.UserLoginSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        serializer = serializers.CustomUserSerializer(user)
        token = RefreshToken.for_user(user)
        token.payload["name"] = user.name
        token.payload["email"] = user.email
        token.payload["is_staff"] = user.is_staff
        token.payload["is_superuser"] = user.is_superuser
        token.payload["last_login"] = user.last_logi
        
        data = dict()
        data["tokens"] = {"refresh": str(token), "access": str(token.access_token)}
        return Response(data, status=status.HTTP_200_OK)
    
class UserLogoutAPIView(GenericAPIView):
        
        permission_classes = (IsAuthenticated,)
        
        def post(self, request, *args, **kwargs):
            try:
                refresh_token = request.data["refresh"]
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response(status=status.HTTP_205_RESET_CONTENT)
            except Exception as e:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            
class UserAPIView(RetrieveUpdateAPIView):
    """
    Get, Update user information
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.CustomUserSerializer

    def get_object(self):
        return self.request.user