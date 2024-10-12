from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime

User = get_user_model()


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_photo = models.ImageField(upload_to='profile_img/', max_length=256, default="download.png", null=True,
                                      blank=True)
    bio = models.CharField(max_length=2000, default=None, blank=True, null=True)
    education = models.CharField(max_length=15, default=None, blank=True, null=True)
    dob = models.DateField(default=None, blank=True, null=True)


class Posts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_image = models.ImageField(upload_to='posts/', max_length=256)
    caption = models.CharField(max_length=2000,blank=True)
    created_at = models.DateTimeField(default=datetime.now(), blank=True)
    no_of_like = models.IntegerField(default=0,blank=True)


class FriendShip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friends")
    friend = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now(), blank=True)


class SavePost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(default=datetime.now(), blank=True)
    
class LikePost(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Posts,on_delete=models.CASCADE)
    liked_at = models.DateTimeField(default=datetime.now(),blank=True)