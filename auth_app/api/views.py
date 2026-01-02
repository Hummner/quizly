from rest_framework.views import APIView
from .serializers import RegisterSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .serializers import CustomTokenSerializer
from .authentication import CookieJWTAuthentication
from rest_framework.permissions import IsAuthenticated

class RegisterView(APIView):
    """
    API endpoint for user registration.
    Handles incoming requests to create a new user.
    """
    def post(self, request):
        """
        Handles POST requests.
        Validates incoming data and creates a new user if valid.
        """
        serilaizer = RegisterSerializer(data=request.data)

        if serilaizer.is_valid(raise_exception=True):
            
            serilaizer.save()

        return Response({"detail": "User created successfully"}, status=status.HTTP_201_CREATED)
    
class LoginView(TokenObtainPairView):
    """
    Handles user login and JWT token generation.

    Extends TokenObtainPairView to authenticate the user,
    return basic user data, and store access and refresh
    tokens securely in HTTP-only cookies.
    """

    serializer_class = CustomTokenSerializer

    def post(self, request, *args, **kwargs):
        """
        Handles POST login requests.

        Authenticates the user, retrieves access and refresh tokens,
        returns user information in the response body, and
        stores the tokens in secure HTTP-only cookies.
        """

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
    """
    Handles access token renewal using the refresh token
    stored in HTTP-only cookies.
    """

    def post(self, request, *args, **kwargs):
        """
        Reads the refresh token from cookies, validates it,
        generates a new access token, and updates the cookie.
        """

        refresh_token = request.COOKIES.get('refresh_token')

        if refresh_token is None:
            return Response(
                {'message': 'Refresh Token is not found'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        serializer = self.get_serializer(data={'refresh': refresh_token})
        serializer.is_valid(raise_exception=True)
        access_token = serializer.validated_data.get('access')

        response = Response({
            'detail': 'Token refreshed',
            'access': access_token
        })

        response.set_cookie(
            key='access_token',
            value=access_token,
            secure=True,
            httponly=True
        )

        return response
    
class LogoutView(APIView):
    """
    API endpoint for user logout.

    Requires authentication and removes JWT tokens
    stored in HTTP-only cookies.
    """

    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Handles POST logout requests.

        Deletes access and refresh tokens from cookies
        and returns a logout confirmation response.
        """

        response = Response({
            "detail": "Log-Out successfully! All Tokens will be deleted. Refresh token is now invalid."
        })

        response.delete_cookie(key='access_token')
        response.delete_cookie(key='refresh_token')

        return response



