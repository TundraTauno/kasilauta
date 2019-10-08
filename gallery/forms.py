from django import forms
from django.forms import ModelForm
from .models import Post, Board

class PostForm(forms.ModelForm):
    class Meta:
        model   = Post
        fields  = '__all__'
        exclude = ['user', 'thread', 'ip_addr']

class BoardForm(forms.ModelForm):
    class Meta:
        model   = Board
        fields  = '__all__'
        exclude = ['user']
