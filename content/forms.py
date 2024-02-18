from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

from django.contrib.auth.models import User
from django.forms.widgets import PasswordInput, TextInput
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'image', 'caption', 'content']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

class CreateUserForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
       model = User
       fields = ['username', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())
        
