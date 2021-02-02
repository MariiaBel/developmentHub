from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey

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

    image = models.ImageField(
        upload_to='posts/', 
        blank=True, 
        null=True
    )

    def __str__(self):
        return self.text[:15]

    class Meta:
        ordering= ["-pub_date"]

class Comment(models.Model):
    text = models.TextField(
        'Текст комментария'
    )
    created = models.DateField(
        'Дата публикации комментария',
        auto_now_add=True
    )
    post = models.ForeignKey(
        Post,
        verbose_name="Пост",
        on_delete = models.CASCADE,
        related_name = "comments"
    )
    author = models.ForeignKey(
        User, 
        verbose_name="Автор комментария",
        on_delete=models.SET_DEFAULT, 
        default = 'Deleted',
        related_name="comments"
    ) 

    def __str__(self):
        return self.text[:15]
    
class Follow(models.Model):
    user = models.ForeignKey(
        User, 
        verbose_name="Подписавшийся пользователь",
        related_name="follower",
        on_delete=models.CASCADE, 
    )
    author = models.ForeignKey(
        User,
        verbose_name="Автор на которого подписались",
        related_name="following",
        on_delete=models.CASCADE, 
    )