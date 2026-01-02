from converter.converter import AudioConverter
from rest_framework import viewsets, status, mixins
from rest_framework.views import APIView
from .serializers import QuizCreateURLSerializer, QuizModelSerializer, QuizCreateSerializer
from rest_framework.response import Response
from .authentication import CookieJWTAuthentication
from rest_framework.permissions import IsAuthenticated
from ..models import Quiz
from .permissions import IsQuizOwner


class CreateQuizView(APIView):
    """
    API endpoint to create a quiz from a YouTube video URL.

    Requires authentication (JWT from cookies). It validates the URL,
    converts the video/audio content into quiz data via AudioConverter,
    saves the quiz + questions, and returns the created quiz.
    """

    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Handles POST requests to create a quiz.

        Steps:
        - Validates and normalizes the YouTube URL
        - Calls the converter to generate quiz JSON
        - Creates the quiz in the database using serializers
        - Returns the created quiz data
        """

        serilaizer_url = QuizCreateURLSerializer(data=request.data)
        serilaizer_url.is_valid(raise_exception=True)
        url = serilaizer_url.validated_data['url']

        converted_json = self.convert_text(request.user.username, url)

        validated_quiz = self.create_quiz(converted_json, url)
        return Response(validated_quiz, status=status.HTTP_201_CREATED)

    def convert_text(self, username, url):
        """
        Runs AudioConverter to generate quiz data (JSON) from the given URL.

        If the converter fails or returns invalid JSON, it returns
        a 422 response describing the issue.
        """

        try:
            created_quiz = AudioConverter(url=url, username=username)
            quiz_json = created_quiz.run()
            return quiz_json
        except:
            return Response(
                {
                    "error": "Invalid AI response",
                    "message": "The generated content could not be parsed as valid JSON."
                },
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

    def create_quiz(self, quiz, url):
        """
        Adds the video URL to the generated quiz data, validates it with
        QuizCreateSerializer, saves it (quiz + questions), and returns the
        final serialized quiz response.
        """

        quiz["video_url"] = url
        create_serializer = QuizCreateSerializer(data=quiz, context={"request": self.request})
        create_serializer.is_valid(raise_exception=True)
        instance = create_serializer.save()

        return QuizModelSerializer(instance).data


class QuizzesViewset(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """
    ViewSet for managing quizzes.

    Supports:
    - list: list quizzes (filtered to the logged-in user)
    - retrieve: get a single quiz (intended to be user-owned)
    - update/partial_update: update a quiz (owner-only)
    - destroy: delete a quiz (owner-only)
    """

    queryset = Quiz.objects.all()
    serializer_class = QuizModelSerializer
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Controls which quizzes are returned depending on the action.

        For listing (and intended retrieve), it returns only quizzes
        owned by the current user and optimizes queries with related loading.
        Otherwise, it falls back to all quizzes.
        """

        if self.action in ['list', 'retrive']:
            qs = Quiz.objects.filter(owner=self.request.user)
            return qs.select_related('owner').prefetch_related('quiz_question')

        return Quiz.objects.all()

    def get_permissions(self):
        """
        Applies object-level permission for destructive or modifying actions.

        Only the quiz owner can update or delete.
        """
        if self.action in ['destroy', 'partial_update', 'update']:
            return [IsQuizOwner()]
        return super().get_permissions()
