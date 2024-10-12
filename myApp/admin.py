from django.contrib import admin
from myApp.models import UserProfile, Posts, FriendShip,SavePost,LikePost


class UserProfile_admin(admin.ModelAdmin):
     list_display = ('user', 'profile_photo', 'bio', 'education', 'dob')


class posts_admin(admin.ModelAdmin):
     list_display = ('post_image', 'caption', 'created_at','no_of_like')

class friendship_admin(admin.ModelAdmin):
     list_display = ('user', 'friend', 'created_at')

class savepost_admin(admin.ModelAdmin):
     list_display = ('user','post','saved_at')

class likpost_admin(admin.ModelAdmin):
     list_display = ('user','post','liked_at')
     
admin.site.register(UserProfile, UserProfile_admin)
admin.site.register(Posts, posts_admin)
admin.site.register(FriendShip, friendship_admin)
admin.site.register(SavePost, savepost_admin)
admin.site.register(LikePost, likpost_admin)
# Register your models here.
