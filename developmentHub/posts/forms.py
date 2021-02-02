from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['group', 'title', 'text', 'image']
        labels = { 
            "group": "Группа", 
            "title": "Название статьи",
            "text": "Текст поста",
            "image": "Изображение",
        } 
        help_texts = { 
            "group": "Укажите группу", 
            "text": "Введите текст вашего нового поста",
        } 

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        labels = {
            "text": "Текст комментария"
        }
        help_texts = {
            "text": "Оставте ваш комментарий"
        }
