
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
import uuid
from users.manager import UserManager
import os
from nanoid import generate
from django.urls import reverse
from django.conf import settings

def get_random_filename(instance, filename):
    # Extract the file extension from the original filename
    ext = filename.split('.')[-1]
    
    # Generate a random filename with uuid
    random_filename = f"{uuid.uuid4()}.{ext}"
    
    # Return the full path, you can customize this path
    return os.path.join('profile-portraits/', random_filename)

def generate_slug():
    return generate(size=6)

class User(AbstractBaseUser, PermissionsMixin):
    public_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    email = models.EmailField(unique=True)

    first_name = models.CharField(max_length = 250)
    
    last_name = models.CharField(max_length = 250)   

    username = models.SlugField(max_length=30, unique=True, null=True)

    is_active = models.BooleanField(default=True)
    
    is_staff = models.BooleanField(default=False)

    avatar = models.ImageField(default='profile-avatar.jpg', upload_to=get_random_filename)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['first_name', 'last_name']

    @property
    def fullname(self):
        return f'{self.first_name} {self.last_name}'
    
    @property
    def avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return settings.MEDIA_URL + 'profile-avatar.jpg'

    def __str__(self):
        return self.email
    
    def get_absolute_url(self):
        return reverse("profile", kwargs={"username": self.username})
    
    def save(self, *args, **kwargs):
        if not self.username:
            username = generate_slug()
            while User.objects.filter(username=username).exists():
                username = generate_slug()
            self.username= username
        super().save(*args, **kwargs)


 

    
