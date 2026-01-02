from rest_framework import serializers, status
from ..models import Quiz, Question
import re

YOUTUBE_REGEX = re.compile(
    r"(https?://)?(www\.)?"
    r"(youtube\.com/(watch\?v=|embed/|shorts/)|youtu\.be/)"
    r"(?P<id>[A-Za-z0-9_-]{11})"
)


class QuizCreateURLSerializer(serializers.Serializer):
    """
    Serializer for validating and normalizing
    a YouTube video URL.
    """

    url = serializers.CharField(write_only=True)

    def validate_url(self, value):
        """
        Validates the URL and converts it
        to a standard YouTube watch URL.
        """
        return self.normalize_youtube_url(value)

    def normalize_youtube_url(self, value: str) -> str:
        """
        Extracts the video ID from different
        YouTube URL formats.
        """
        match = re.search(
            r"(?:v=|youtu\.be/|embed/|shorts/)([A-Za-z0-9_-]{11})",
            value
        )
        if not match:
            raise serializers.ValidationError(
                "Enter a valid YouTube video URL."
            )

        video_id = match.group(1)
        return f"https://www.youtube.com/watch?v={video_id}"


class QuizQuestionsSerializer(serializers.ModelSerializer):
    """
    Serializer for quiz questions.
    """

    question_options = serializers.ListField(
        child=serializers.CharField()
    )

    class Meta:
        model = Question
        fields = [
            'id',
            'question_options',
            'answer',
            'created_at',
            'updated_at',
            'question_title'
        ]


class QuizModelSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying quiz data
    including related questions.
    """

    questions = QuizQuestionsSerializer(
        source="quiz_question",
        many=True,
        read_only=True
    )

    class Meta:
        model = Quiz
        fields = [
            'id',
            'title',
            'questions',
            'created_at',
            'updated_at',
            'video_url',
            'description'
        ]
        read_only_fields = ['created_at', 'updated_at', 'video_url']


class QuizCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a quiz
    with nested questions.
    """

    questions = QuizQuestionsSerializer(many=True)

    def create(self, validated_data):
        """
        Creates a quiz and its related questions.
        """
        questions_data = validated_data.pop('questions')
        user = self.context['request'].user
        quiz = Quiz.objects.create(owner=user, **validated_data)

        for q in questions_data:
            Question.objects.create(quiz=quiz, **q)

        return quiz

    class Meta:
        model = Quiz
        fields = [
            'id',
            'title',
            'owner',
            'questions',
            'created_at',
            'updated_at',
            'video_url',
            'description'
        ]
        extra_kwargs = {
            'questions': {'read_only': True},
            'owner': {'read_only': True}
        }
