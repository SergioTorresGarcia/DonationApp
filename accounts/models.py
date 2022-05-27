from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.urls import reverse

# Create your models here.

class AccountManager(BaseUserManager):
    """Define a model manager for User model with no username field."""
    def _create_user(self, email, password=None, **extra_fields):
        """Create and save a User with the given email and password."""

        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class Account(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = AccountManager()


class Category(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Institution(models.Model):
    TYPE_CHOICES = (
        ('1', "Fundacja"),
        ('2', "Organizacja pozarządowa"),
        ('3', "Zbiórka lokalna"),
    )

    name = models.CharField(max_length=32)
    description = models.TextField()
    type = models.CharField(
        max_length = 20,
        choices = TYPE_CHOICES,
        default = '1'
        )
    category = models.ManyToManyField(Category)

    def __str__(self):
        return self.name


class Donation(models.Model):
    quantity = models.IntegerField()
    categories = models.ManyToManyField('Category')
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    phone_number = models.IntegerField()
    address = models.CharField(max_length=64)
    city = models.CharField(max_length=20)
    zip_code = models.IntegerField()
    pick_up_date = models.DateField(auto_now=False)
    pick_up_time = models.TimeField(auto_now=False)
    pick_up_comment = models.TextField(blank=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    is_taken = models.BooleanField(default=False)

    def __str__(self):
        return self.user

    def get_absolute_url(self):
        return reverse('user-detail', args=(self.id,))
