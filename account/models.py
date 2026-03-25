from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(User):

    class Meta: 
        verbose_name = 'UserProfile'
        verbose_name_plural = 'UserProfiles'