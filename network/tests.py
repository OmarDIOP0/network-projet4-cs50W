from django.test import TestCase,Client

from .models import User,Post,Follow
# Create your tests here.

class Network(TestCase):
    def setUp(self):
        user = User.objects.create(username="Omar", email="odiop@gmail.com")
        fist_post = Post.objects.create(content="my_first_post",author=user)

    def test_create_user(self):
        user = User.objects.get(username="Omar")
        self.assertEqual(user.username,"Omar")
        self.assertEqual(user.email,"odiop@gmail.com")

    def test_create_post(self):
        post = Post.objects.get(content="my_first_post")
        self.assertEqual(post.content,"my_first_post")
        self.assertEqual(post.author.username,"Omar")

    def test_all_posts(self):
        c = Client()
        response = c.get('/')
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.context['posts'].count(),1)

    




    
