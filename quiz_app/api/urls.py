from django.urls import path
from .views import QuizzesViewset, CreateQuizView
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register(r"quizzes", QuizzesViewset, basename="quizzes")

urlpatterns = [
    path('createQuiz/', CreateQuizView.as_view(), name='create_quiz')
]

urlpatterns += router.urls