from django.urls import path
from .views import QuizzesViewset
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register(r"quizzes", QuizzesViewset, basename="quizzes")

urlpatterns = router.urls