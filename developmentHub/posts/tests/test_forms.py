import django
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from ..models import Post

class FormTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = get_user_model().objects.create(username = "test-user")
        Post.objects.create(
            title = 'Тестовый заголовок поста',
            text = 'Текст тестового поста',
            author = cls.user
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_creat_new_post(self):
        """Adds new post via the form"""    
        posts_count = Post.objects.count()
        form_data = {
            "text": 'Текст тестовой формы',
            "author": FormTest.user
        }
        response = self.authorized_client.post(
            reverse('new_post'),
            data=form_data,
            follow=True
        )
        new_post = Post.objects.filter(text = "Текст тестовой формы")
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(new_post.exists())

