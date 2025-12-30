from django.urls import path
from .views import QuziCreateView, QuizzesViewset
from rest_framework.routers import SimpleRouter

router = SimpleRouter
router.register(r"quizess", QuizzesViewset, basename="quizess")

urlpatterns = router.urls