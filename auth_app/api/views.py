from rest_framework.views import APIView
from .serializers import RegisterSerializer
from rest_framework.response import Response
from rest_framework import status

class RegisterView(APIView):
    def post(self, request):
        serilaizer = RegisterSerializer(data=request.data)

        if serilaizer.is_valid(raise_exception=True):
            
            serilaizer.save()

        return Response({"detail": "User created successfully"}, status=status.HTTP_201_CREATED)
    
class LoginView(APIView):
    pass