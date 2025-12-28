from rest_framework.views import APIView
from .serializers import RegisterSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
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
        user = kwargs['user']

        response.set_cookie(
            key='access_token',
            value=access_token,
            secure=True,
            httponly=True,
            samesite=True,
        )

        response.set_cookie(
            key='refresh_token',
            value=refresh_token,
            secure=True,
            httponly=True,
            samesite=True,
        )
        

        response = {}
        return response