from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Post, Group

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
                print("---->>>", page, url)  
                self.assertEqual(page[0].text, "Текст тестовой статьи") 
                self.assertEqual(page[0].author, self.user)   
                self.assertEqual(page[0].group, self.group)    