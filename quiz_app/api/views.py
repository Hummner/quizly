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
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serilaizer_url = QuizCreateURLSerializer(data=request.data)
        serilaizer_url.is_valid(raise_exception=True)
        url = serilaizer_url.validated_data['url']

        converted_json = self.convert_text(request.user.username, url)

        validated_quiz = self.create_quiz(converted_json, url)
        return Response(validated_quiz, status=status.HTTP_201_CREATED)
    
    def convert_text(self, username, url):
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
                   viewsets.GenericViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizModelSerializer
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        if self.action in ['list', 'retrive']:
            qs = Quiz.objects.filter(owner=self.request.user)
            return qs.select_related('owner').prefetch_related('quiz_question')
        
        return Quiz.objects.all()
    

    def get_permissions(self):
        if self.action in ['destroy', 'partial_update', 'update']:
            return [IsQuizOwner()]
        return super().get_permissions()