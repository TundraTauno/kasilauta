from django import forms
from django.forms import ModelForm
from .models import Post, Board

from captcha.fields import ReCaptchaField

class PostForm(forms.ModelForm):
    captcha = ReCaptchaField() 
    class Meta:
        model   = Post
        fields  = '__all__'
        exclude = ['user', 'thread', 'ip_addr']

class BoardForm(forms.ModelForm):
    captcha = ReCaptchaField() 
    class Meta:
        model   = Board
        fields  = '__all__'
        exclude = ['user']
