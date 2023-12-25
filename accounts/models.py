from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils import timezone
from PIL import Image
from .manager import MyUserManager

# Create your models here.


class User(AbstractBaseUser):
    email = models.CharField(max_length=255, unique=True)
    username = models.CharField(max_length=50, unique=True)
    avatar = models.ImageField(upload_to='image/avatars/%Y/%m/%d/', default='image/avatars/default.png')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    
    objects = MyUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def __str__(self) -> str:
        return self.email
    
    def has_perm(self, perm, obj=None):
        if self.is_active and self.is_admin:
            return True
        
        return False
    
    def has_module_perms(self, app_label):
        if self.is_admin:
            return True
        
        return False
    
    @property
    def is_staff(self):
        return self.is_admin