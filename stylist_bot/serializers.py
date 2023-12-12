from rest_framework import serializers
from stylist_bot.models import TelegramUser, Image, SignIn


class TelegramUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramUser
        fields = "__all__"


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"


class SignInSerializer(serializers.ModelSerializer):
    class Meta:
        model = SignIn
        fields = "__all__"
