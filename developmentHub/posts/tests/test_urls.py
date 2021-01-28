from django.http import response
from django.test import TestCase, Client
from django.contrib.auth import get_user_model

from ..models import Group

class URLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Group.objects.create(
            title = "Тестовая группа",
            slug = "group-test-slug",
            description = 'Описание тестовой группы',
        )

    def setUp(self):
        # self.fields_for_all_client = {'/',}
        # self.fields_for_authorized_client = {'/group/group-test-slug/',  '/new/',}
        self.fields_url = {
            '/': {
                'access': 'all',
                'template': 'index.html'
            },
            '/new/': {
                'access': 'authorized',
                'template': 'new-post.html'
            },
            '/group/group-test-slug/': {
                'access': '',
                'template': 'group.html'
            },
        }
        self.guest_client = Client()
        self.user = get_user_model().objects.create(username='TestUserName')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_url_exists_and_correct(self):
        for value, field in self.fields_url.items():
            with self.subTest():
                if field['access'] == 'authorized':
                    response = self.authorized_client.get(value)
                    self.assertEqual(response.status_code, 200)
                    self.assertTemplateUsed(response, field['template'])
                else: 
                    response = self.guest_client.get(value)
                    self.assertEqual(response.status_code, 200)
                    self.assertTemplateUsed(response, field['template'])

    def test_url_redirect_for_unauthorized(self):
        for value, field in self.fields_url.items():
            with self.subTest():
                if field['access'] == 'authorized':
                    response = self.guest_client.get(value, follow=True)
                    redirect = f'/auth/login/?next={value}' 
                    self.assertRedirects(response, redirect)

    # def test_url_exists_for_authorized_client(self):
    #     for value in self.fields_for_authorized_client:
    #         with self.subTest():
    #             responce = self.authorized_client.get(value)
    #             self.assertEqual(responce.status_code, 200)

    # def test_author(self):
    #     """Checks url for author page. Status code should be 200."""    
    #     response = self.guest_client.get('/author/')
    #     self.assertEqual(response.status_code, 200)
    # def test_technology(self):
    #     """Checks url for technologies page. Status code should be 200."""  
    #     response = self.guest_client.get('/technology/')
    #     self.assertEqual(response.status_code, 200)

