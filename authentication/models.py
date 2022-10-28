from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
# from django.contrib.authentication import get_user_model
import uuid
from datetime import datetime

# User = get_user_model()


class ProfileManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User
        """
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        email = email.lower()

        user = self.model(
            email=email,
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser
        """
        user = self.create_user(
            email,
            password=password,
        )

        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class Profile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, max_length=255)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = ProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

'''
# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField(default=None)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='profile_images', default='blank-profile-picture.png')
    gender = models.IntegerField(default=None)
    birthday = models.DateField(auto_now=True)
    phone = models.CharField(max_length=32, blank=True)
    website = models.CharField(max_length=128, blank=True)
    country_id = models.IntegerField(default=None)
    city_id = models.IntegerField(default=None)
    citizenship = models.CharField(max_length=32, blank=True)
    tin = models.IntegerField(default=None)
    address = models.CharField(max_length=256, blank=True)
    university = models.CharField(max_length=128, blank=True)
    speciality = models.CharField(max_length=64, blank=True)
    ending_year = models.DateField(auto_now=True)
    employment_id = models.IntegerField(default=None)
    skills = models.TextField(blank=True)
    work_experience = models.IntegerField(default=None)
    achievements = models.TextField(blank=True)
    hackathons = models.IntegerField(default=None)
    is_active = models.BooleanField(default=True)
    role = models.CharField(max_length=128, blank=True)
    has_team = models.BooleanField(default=False)
    has_project = models.BooleanField(default=False)
    has_company = models.BooleanField(default=False)
    has_patent = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    image = models.ImageField(upload_to='post_images')
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    no_of_likes = models.IntegerField(default=0)

    def __str__(self):
        return self.user


class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username


class FollowersCount(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)

    def __str__(self):
        return self.user
'''
