from rest_framework import viewsets

from stylist_bot.models import TelegramUser
from stylist_bot.serializers import TelegramUserSerializer


class TelegramUserViewSet(viewsets.ModelViewSet):
    queryset = TelegramUser.objects.all()
    serializer_class = TelegramUserSerializer