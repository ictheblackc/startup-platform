from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models


class ProfileManager(BaseUserManager):
    def create_user(self, email, bio, phone, avatar, gender, date_of_birth, website, country_id, city_id, citizenship,
                    tin, address, university, speciality, ending_year, employment_id, skills, work_experience,
                    achievements, hackathons, role, is_active, is_admin, has_team, has_project, has_company, has_patent,
                    password=None):
        """
        Creates and saves a User
        """
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        email = email.lower()

        user = self.model(email=email, phone=phone, bio=bio, avatar=avatar, gender=gender, date_of_birth=date_of_birth,
                          website=website, country_id=country_id, city_id=city_id, citizenship=citizenship, tin=tin,
                          address=address, university=university, speciality=speciality, ending_year=ending_year,
                          employment_id=employment_id, skills=skills, work_experience=work_experience,
                          achievements=achievements, hackathons=hackathons, role=role, is_active=is_active,
                          is_admin=is_admin, has_team=has_team, has_project=has_project, has_company=has_company,
                          has_patent=has_patent)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, bio, phone, avatar, gender, date_of_birth, website, country_id, city_id,
                         citizenship, tin, address, university, speciality, ending_year, employment_id, skills,
                         work_experience, achievements, hackathons, role, is_active, is_admin, has_team, has_project,
                         has_company, has_patent, password=None):
        """
        Creates and saves a superuser
        """
        user = self.create_user(email=email, password=password, phone=phone, bio=bio, avatar=avatar, gender=gender,
                                date_of_birth=date_of_birth, website=website, country_id=country_id, city_id=city_id,
                                citizenship=citizenship, tin=tin, address=address, university=university,
                                speciality=speciality, ending_year=ending_year, employment_id=employment_id,
                                skills=skills, work_experience=work_experience, achievements=achievements,
                                hackathons=hackathons, role=role, is_active=is_active, is_admin=is_admin,
                                has_team=has_team, has_project=has_project, has_company=has_company,
                                has_patent=has_patent)

        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class Profile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='profile_images', default='blank-profile-picture.png')
    gender = models.IntegerField(default=None)
    date_of_birth = models.DateField(auto_now=True)
    website = models.CharField(max_length=255, blank=True)
    country_id = models.IntegerField(default=None)
    city_id = models.IntegerField(default=None)
    citizenship = models.CharField(max_length=255, blank=True)
    tin = models.IntegerField(default=None)
    address = models.CharField(max_length=255, blank=True)
    university = models.CharField(max_length=255, blank=True)
    speciality = models.CharField(max_length=255, blank=True)
    ending_year = models.DateField(auto_now=True)
    employment_id = models.IntegerField(default=None)
    skills = models.TextField(blank=True)
    work_experience = models.IntegerField(default=None)
    achievements = models.TextField(blank=True)
    hackathons = models.IntegerField(default=None)
    role = models.CharField(max_length=255, blank=True)
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
