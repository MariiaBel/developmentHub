from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = {'group', 'text'}
        labels = { 
            "group": "Группа", 

            "text": "Текст поста"
        } 
        help_texts = { 
            "group": "Укажите группу", 
            "text": "Введите текст вашего нового поста" 
        } 