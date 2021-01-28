from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Group(models.Model):
    title = models.CharField(
        "Название группы",
        max_length=200,
        help_text= "Дайте назание группе",
        )
    slug = models.SlugField(
        "Слаг",
        unique=True,
        help_text = ('Укажите адрес для группы. Используйте '
                     'только латиницу, цифры, дефисы и знаки '
                     'подчёркивания'),
        )
    description = models.TextField(
        "Описание группы"
        )
    
    def __str__(self):
        return self.title 

class Post(models.Model):
    title = models.CharField(
        "Название статьи",
        max_length=200,
        help_text= "Дайте название статье",
        blank=True, 
        null=True,
    )
    text = models.TextField(
        "Текст статьи"
    )
    pub_date = models.DateTimeField(
        "Дата публикации", 
        auto_now_add=True
    )
    author = models.ForeignKey(
        User, 
        verbose_name="Автор статьи",
        on_delete=models.CASCADE, 
        related_name="posts"
    ) 
    group = models.ForeignKey(
        Group, 
        verbose_name="Название группы",
        help_text="Укажите группу для статьи",
        on_delete=models.SET_NULL,
        blank=True, 
        null=True,
        related_name="posts"
    )
    def __str__(self):
        return self.text[:15]

    class Meta:
        ordering= ["-pub_date"]

