import re

from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from captcha.fields import CaptchaField, CaptchaTextInput
from django.forms import ModelForm

from .models import Post, Comments


class ContactForm(forms.Form):
    subject = forms.CharField(
        label='Тема',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    content = forms.CharField(
        label='Текст',
        widget=forms.Textarea(attrs={'class': 'form-control',  'rows':5})
    )
    captcha = CaptchaField(widget=CaptchaTextInput)


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Имя Пользователя',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )



class UserRegisterForm(UserCreationForm):
    username = forms.CharField(
        label='Имя Пользователя',
        widget=forms.TextInput(attrs={'class':'form-control', 'autocomlete': "off"})
    )
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label='Повторите пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label='E-mail',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class PostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())
    # photo = forms.FileField(widget=forms.FileInput(attrs={'id': 'one_image'}))
    class Meta:
        model = Post
        exclude = ['author']
        fields = ['title', 'content', 'photo', 'is_published', 'category']
        #fields = '__all__'
        # widgets для название класса в html

        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'content': forms.Textarea(attrs={'class':'form-control', 'rows':5}),
            'category': forms.Select(attrs={'class':'form-control'}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if re.match(r'\d', title):
            raise ValidationError('Значение не дожлно начинаться с цифры')
        return title

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


