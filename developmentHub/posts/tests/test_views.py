from django.contrib import auth
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Post, Group, Follow

class ViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = get_user_model().objects.create(username = "test-user")
        cls.group = Group.objects.create(
            title = "Тестовая группа",
            slug = "group-test-slug",
            description = 'Описание тестовой группы',
        )
        Post.objects.create(
            title="Заголовок тестовой статьи",
            text="Текст тестовой статьи",
            author = cls.user,
            group = cls.group,
        )

    def setUp(self):
        self.url_fields = {
            '/': {
                'name': reverse('index'),
                'template': 'index.html',
            },
            '/group/group-test-slug/': {
                'name': reverse('group', kwargs={'slug': 'group-test-slug'}),
                'template': 'group.html',
            },
            '/new/': {
                'name':reverse('new_post'),
                'template': 'new-post.html',
            },
        }

        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.guest_client = Client();

    def test_page_template(self):
        """Checks templates and context for post pages"""
        for url, field in self.url_fields.items():
            with self.subTest(url = url):
                response = self.authorized_client.get(field['name'])
                self.assertTemplateUsed(response,field['template'] )

    def test_homepage_correct_context(self):
        """Index page has newly created post"""  
        field_urls = { reverse('index'), }
        
        for url in field_urls:
            with self.subTest(url = url):
                response = self.guest_client.get(url)
                page = response.context.get('page')   
                self.assertEqual(page[0].text, "Текст тестовой статьи") 
                self.assertEqual(page[0].author, self.user)   
                self.assertEqual(page[0].group, self.group)    

class FollowTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user1 = get_user_model().objects.create(username = "test-user1")
        cls.user2 = get_user_model().objects.create(username = "test-user2")

    def setUp(self):
        self.authorized_client1 = Client()
        self.authorized_client1.force_login(self.user1)
        self.authorized_client2 = Client()
        self.authorized_client2.force_login(self.user2)

    def test_user_subscribes(self):
        """Authorised user can subscribe to author"""
        params = {
            "username": self.user1.username,
        }
        self.authorized_client2.get(reverse('profile_follow', kwargs=params))
        self.assertTrue(Follow.objects.filter(author=self.user1, user=self.user2).exists())
    def test_user_unsubscride(self):
        """Authorised user can unsubscribe from author"""
        Follow.objects.create(author=self.user1, user=self.user2)
        params = {
            "username": self.user1.username,
        }
        self.authorized_client2.get(reverse('profile_unfollow', kwargs=params))
        self.assertFalse(Follow.objects.filter(author=self.user1, user=self.user2).exists())