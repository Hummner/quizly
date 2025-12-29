from rest_framework.views import APIView
from .serializers import RegisterSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .serializers import CustomTokenSerializer

class RegisterView(APIView):
    def post(self, request):
        serilaizer = RegisterSerializer(data=request.data)

        if serilaizer.is_valid(raise_exception=True):
            
            serilaizer.save()

        return Response({"detail": "User created successfully"}, status=status.HTTP_201_CREATED)
    
class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        access_token = response.data.get('access')
        refresh_token = response.data.get('refresh')
        user = response.data['user']

        response = Response({
            'detail': 'Login successfully',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email}
        }, status=status.HTTP_200_OK)

        response.set_cookie(
            key='access_token',
            value=access_token,
            secure=True,
            httponly=True
        )

        response.set_cookie(
            key='refresh_token',
            value=refresh_token,
            secure=True,
            httponly=True
        )
        
        return response
    
class RefreshToken(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        
        refresh_token = request.COOKIES.get('refresh_token')

        if refresh_token is None:
            raise Response({'message': 'Refresh Token is not found'})
        
        serializer = self.get_serializer(data={'refresh': refresh_token})
        serializer.is_valid(raise_exception=True)
        access_token= serializer.validated_data.get('access')

        response = Response({
              "detail": "Token refreshed",
                "access": access_token
        })

        response.set_cookie(
            key='access_token',
            value=access_token,
            secure=True,
            httponly=True
        )

        return response
