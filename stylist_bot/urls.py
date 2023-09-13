from django.urls import path, include
from rest_framework.routers import DefaultRouter
from stylist_bot.views import TelegramUserViewSet

router = DefaultRouter()
router.register(r'telegram-users', TelegramUserViewSet)

urlpatterns = [
    path("api/", include(router.urls))
]