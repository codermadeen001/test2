from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field is required.")
        email = self.normalize_email(email)
        extra_fields.setdefault('role', 'agent')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('role', 'admin')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('agent', 'Field Agent'),
    ]
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=True, blank=True, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    profile_picture = models.CharField(max_length=255, default='https://drivemate-1.onrender.com/media/dp.jpg', blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='agent')
    created_at = models.DateTimeField(default=timezone.now)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
  


    def __str__(self):
        return f"{self.id} {self.role} <{self.email}>"

