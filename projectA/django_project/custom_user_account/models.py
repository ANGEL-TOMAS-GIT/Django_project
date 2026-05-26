from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, email, phone_number, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is Required')
        if not phone_number:
            raise ValueError('Phone Number is Required')
        email = self.normalize_email(email)
        user = self.model(email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        return self.create_user(email, phone_number, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name='Email')
    phone_number = models.CharField(max_length=10, unique=True, verbose_name='Phone number')
    first_name = models.CharField(max_length=30, blank=True, verbose_name='First name')
    last_name = models.CharField(max_length=50, blank=True, verbose_name='Last name')
    date_of_birth = models.DateField(null=True, blank=True, verbose_name='Birthday')
    profile_image = models.ImageField(upload_to='profile_avatars/', blank=True, null=True)
    is_staff = models.BooleanField(default=False, verbose_name='Personal status')
    is_active = models.BooleanField(default=True, verbose_name='Active Account')
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='Date Registration')
    pref_lang = models.CharField(max_length=10, choices=[
        ('es', 'Spanisch'),
        ('en', 'English')
    ], default='en', verbose_name='language')

    object = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email
