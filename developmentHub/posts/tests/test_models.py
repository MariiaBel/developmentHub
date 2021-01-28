from django.test import TestCase
from django.contrib.auth import get_user_model

from ..models import Post, Group

User = get_user_model();

class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username = "Юзер")
        cls.post = Post.objects.create(
            title="Заголовок тестовой статьи",
            text="Текст тестовой статьи",
            author = cls.user,
        )
        cls.group = Group.objects.create(
            title = "Название тестовой группы",
            slug = "test-slug",
            description = "Описание тестовой группы",
        )
    
    def setUp(self):
        self.post = PostModelTest.post
        self.group = PostModelTest.group

    def test_verbose_name_post(self):  
        """Checks verbose names for post"""      
        field_verboses = {
            "title": "Название статьи",
            "text": "Текст статьи",
            "pub_date": "Дата публикации",
            "group": "Название группы",
            "author": "Автор статьи",
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(self.post._meta.get_field(value).verbose_name, expected)

    def test_verbose_name_group(self):   
        """Checks verbose names for group"""       
        field_verboses = {
            "title": "Название группы",
            "slug": "Слаг",
            "description": "Описание группы",
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(self.group._meta.get_field(value).verbose_name, expected)

    def test_help_text_post(self):
        """Checks help text for post"""     
        field_help_text = {
            "title": "Дайте название статье",
            "group": "Укажите группу для статьи",
        } 
        for value, expected in field_help_text.items():
            with self.subTest(value=value):
                self.assertEqual(self.post._meta.get_field(value).help_text, expected)

    def test_help_text_group(self):
        """Checks help text for group"""     
        field_help_text = {
            "title": "Дайте назание группе",
            "slug": ('Укажите адрес для группы. Используйте '
                     'только латиницу, цифры, дефисы и знаки '
                     'подчёркивания'),
        } 
        for value, expected in field_help_text.items():
            with self.subTest(value=value):
                self.assertEqual(self.group._meta.get_field(value).help_text, expected)           

    def test_str_post(self):
        """Checks __str__ for post"""
        expected_str = self.post.text[:15]
        self.assertEqual(expected_str, str(self.post))

    def test_str_group(self):
        """Checks __str__ for group""" 
        expected_str = self.group.title
        self.assertEqual(expected_str, str(self.group))   