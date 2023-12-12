from rest_framework import viewsets

from stylist_bot.models import TelegramUser, Image, SignIn
from stylist_bot.serializers import TelegramUserSerializer, ImageSerializer, SignInSerializer
from django.views import generic


class TelegramUserViewSet(viewsets.ModelViewSet):
    queryset = TelegramUser.objects.all()
    serializer_class = TelegramUserSerializer


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


class SignInViewSet(viewsets.ModelViewSet):
    queryset = SignIn.objects.all()
    serializer_class = SignInSerializer


class SignInListView(generic.ListView):
    model = SignIn
    template_name = "sign_in/customers.html"
    queryset = SignIn.objects.all()

class SignInDetailView(generic.DetailView):
    model = SignIn
    template_name = 'sign_in/customer_detail.html'
    context_object_name = "customer"
