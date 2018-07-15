from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core.validators import ValidationError,RegexValidator


def create_profile(sender, *args, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])


post_save.connect(create_profile, sender=User)


class Country(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    pic = models.ImageField(blank=True, null=True, upload_to='profile_image')
    facebook = models.URLField(blank=True, null=True)
    google = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    biography = models.TextField(blank=True, null=True, max_length=200)
    completed=models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)