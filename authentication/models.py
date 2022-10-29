from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models


class ProfileManager(BaseUserManager):
    def create_user(self, username, email, phone=123, gender=None, date_of_birth=None, website=None,
                    country_id=None, city_id=None,
                    citizenship=None,
                    tin=None, address=None, university=None, speciality=None, ending_year=None, employment_id=None,
                    skills=None, work_experience=None,
                    achievements=None, hackathons=None, role=None, has_team=False, has_project=False, has_company=False,
                    has_patent=False,
                    password=None, bio=None):
        """
        Creates and saves a User
        """
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        email = email.lower()

        user = self.model(username=username, email=email, phone=phone, bio=bio, gender=gender,
                          date_of_birth=date_of_birth, website=website, country_id=country_id, city_id=city_id,
                          citizenship=citizenship, tin=tin, address=address, university=university,
                          speciality=speciality, ending_year=ending_year, employment_id=employment_id, skills=skills,
                          achievements=achievements, hackathons=hackathons, role=role, has_team=has_team, has_project=has_project, has_company=has_company,
                          has_patent=has_patent, work_experience=work_experience)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, bio, phone, gender, date_of_birth, website, country_id, city_id,
                         citizenship, tin, address, university, speciality, ending_year, employment_id, skills,
                         work_experience, achievements, hackathons, role, has_team, has_project,
                         has_company, has_patent, password=None):
        """
        Creates and saves a superuser
        """
        user = self.create_user(username=username, email=email, password=password, phone=phone, bio=bio,
                                date_of_birth=date_of_birth, website=website, country_id=country_id, city_id=city_id,
                                citizenship=citizenship, tin=tin, address=address, university=university,
                                speciality=speciality, ending_year=ending_year, employment_id=employment_id,
                                skills=skills, work_experience=work_experience, achievements=achievements,
                                hackathons=hackathons, role=role,
                                has_team=has_team, has_project=has_project, has_company=has_company,
                                has_patent=has_patent, gender=gender)

        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class Profile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='profile/avatars', default='blank-profile-avatar.png')
    background_profile_photo = models.ImageField(upload_to='profile/backgrounds', default='blank-profile-background.jpg')
    gender = models.IntegerField(default=None, null=True)
    date_of_birth = models.DateField(auto_now=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    country_id = models.IntegerField(default=None, null=True)
    city_id = models.IntegerField(default=None, null=True)
    citizenship = models.CharField(max_length=255, blank=True, null=True)
    tin = models.IntegerField(default=None, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    university = models.CharField(max_length=255, blank=True, null=True)
    speciality = models.CharField(max_length=255, blank=True, null=True)
    ending_year = models.DateField(auto_now=True)
    employment_id = models.IntegerField(default=None, null=True)
    skills = models.TextField(blank=True, null=True)
    work_experience = models.IntegerField(default=None, null=True)
    achievements = models.TextField(blank=True, null=True)
    hackathons = models.IntegerField(default=None, null=True)
    role = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    has_team = models.BooleanField(default=False)
    has_project = models.BooleanField(default=False)
    has_company = models.BooleanField(default=False)
    has_patent = models.BooleanField(default=False)

    objects = ProfileManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'name', 'phone', 'date_of_birth', 'citizenship', 'has_team', 'role', 'has_company',
                       'has_patent']

    def __str__(self):
        return self.username


'''
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
