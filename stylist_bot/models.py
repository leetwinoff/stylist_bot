from django.db import models


class TelegramUser(models.Model):
    user_id = models.IntegerField(unique=True)
    username = models.CharField(max_length=100, null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)


class Image(models.Model):
    image_file = models.ImageField(upload_to="images/")


class SignIn(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    tg_id = models.IntegerField(null=True, blank=True)
    tg_username = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    service_choice = models.CharField(max_length=100, null=True, blank=True)





