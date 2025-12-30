from rest_framework import serializers
from ..models import Quiz, Question


class QuizCreateURLSerializer(serializers.Serializer):

    url = serializers.CharField(write_only=True)

    def validate(self, attrs):

        return super().validate(attrs)
    


class QuizQuestionsSerializer(serializers.ModelSerializer):
    question_options = serializers.ListField(
        child=serializers.CharField()
    )

    class Meta:
        model = Question
        fields = ['id','question_options', 'answer', 'created_at', 'updated_at', 'question_title']   


class QuizModelSerializer(serializers.ModelSerializer):
    questions = QuizQuestionsSerializer(source="quiz_question", many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'questions', 'created_at', 'updated_at', 'video_url', 'description']




class QuizCreateSerializer(serializers.ModelSerializer):
        questions = QuizQuestionsSerializer(many=True)
        
        def create(self, validated_data):
            questions_data = validated_data.pop('questions')
            quiz = Quiz.objects.create(**validated_data)

            for q in questions_data:
                Question.objects.create(quiz=quiz, **q)

             

            return quiz

        class Meta:
            model = Quiz
            fields = ['id', 'title', 'questions', 'created_at', 'updated_at', 'video_url', 'description']
            extra_kwargs = {
                'questions': {
                    'read_only': True
                }
            }
