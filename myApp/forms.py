from django.forms import ModelForm,widgets
from myApp.models import UserProfile, Posts
from django import forms

class DateInput(forms.DateInput):
     input_type = 'date'

class profileform(ModelForm):
     class Meta:
          model = UserProfile
          fields = ['profile_photo', 'bio', 'education', 'dob']
          widgets = {
               'profile_photo': widgets.FileInput(
                    attrs={'id': 'profile_photo', 'style': 'display: none;', 'accept': 'image/jpg image/png'}),
               'bio': widgets.TextInput(attrs={'class': ' mb-3', 'id': 'bio', 'required': 'True'}),
               'dob': forms.DateInput(attrs={'type':'date'}),
               'education': widgets.TextInput(attrs={'class': 'mb-3'}),
          }          

class postForm(ModelForm):
     class Meta:
          model = Posts
          fields = ['post_image','caption']
          widgets = {
               'username' : widgets.TextInput(attrs={'class' : 'hidden'}),
               'post_image' : widgets.FileInput(attrs={'id':'post_image', 'style':'display: none;','accept':'image/jpg image/png'}),
               'caption': widgets.TextInput(attrs={'autocomplete':'off','id': 'caption'}),
          }

class savePostForm(ModelForm):
     class Meta:
          fields = ['post','saved_at']