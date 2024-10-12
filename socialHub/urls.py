"""socialHub URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from socialHub import views
from django.conf.urls.static import static
from django.conf import settings
from django.urls import reverse

urlpatterns = [
    path('admin/', admin.site.urls),
    path('socialHub/',views.socialHub,name='socialHub'),
    path('login/',views.login_page,name="login_page"),
    path('signup/',views.signup,name="signup"),
    path('home/',views.home,name="home"),
    path('profile_data/',views.profile_data,name="profile_data"),
    path('profile/<str:username>',views.profile,name="profile"),
    path('logout_view/',views.logout_view,name="logout_view"),
    path('add_friend/<int:friend_id>',views.add_friend,name="add_friend"),
    path('edit_profile/',views.edit_profile,name="edit_profile"),
    path('savepost/<int:post_id>',views.savepost,name="savepost"),
    path('likepost/<int:post_id>',views.likepost,name="likepost"),
    path('delete_post/<int:post_id>',views.delete_post,name="delete_post"),
    path('delete_account/<int:user_id>',views.delete_account,name="delete_account"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)