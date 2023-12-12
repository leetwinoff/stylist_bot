from django.urls import path, include
from rest_framework.routers import DefaultRouter
from stylist_bot.views import TelegramUserViewSet, ImageViewSet, SignInViewSet, SignInListView, SignInDetailView

router = DefaultRouter()
router.register(r"telegram-users", TelegramUserViewSet)
router.register("images", ImageViewSet)
router.register("signin", SignInViewSet)

urlpatterns = [
    path("customer_list/", SignInListView.as_view(), name="customers"),
    path("customer/<int:pk>/", SignInDetailView.as_view(), name="customer-detail"),
    path("api/", include(router.urls))
]