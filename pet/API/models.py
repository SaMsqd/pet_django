from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken


class CustomUserManager(BaseUserManager):
    def get_or_create(self, email=None, **kwargs):
        allowed_kwargs = ['email', 'password']
        if email is not None:
            try:
                user_obj = super(CustomUserManager, self).get(email=email)
                if kwargs:
                    for k, v in kwargs.items():
                        setattr(user_obj, k, v)
                    user_obj.save()
            except ObjectDoesNotExist:
                email = self.normalize_email(email)
                user_obj = self.model(email=email)
                password = kwargs.pop('password', None)
                if password is not None:
                    user_obj.set_password(password)
                if kwargs:
                    for k, v in kwargs.items():
                        if k in allowed_kwargs:
                            setattr(user_obj, k, v)
                user_obj.save()
        else:
            return False
        return user_obj

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        user = self.create_user(email, password, **extra_fields)
        return user


# Create your models here.
class User(AbstractUser):
    id = models.IntegerField(primary_key=True, auto_created=True, help_text='А нехуй сюда лезть')
    email = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=128)
    username = models.CharField(max_length=128, blank=True, unique=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']

    objects = CustomUserManager()

    @property
    def jwt_tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


class Film(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    title = models.CharField(max_length=128)
    year = models.IntegerField()
    genre = models.CharField(max_length=128)
    duration = models.IntegerField()
    rating = models.IntegerField()

    def __str__(self):
        return {'title': self.title}


class Review(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=128)
    rating = models.IntegerField()
