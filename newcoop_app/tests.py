from django.test import TestCase
from django.urls import reverse


# Create your tests here.

class IndexTests(TestCase):

    def test_default_elements(self):
        response = self.client.get(reverse('newcoop_app:index'))
        self.assertContains(response, 'Game')
        self.assertContains(response, 'Platform')
        self.assertContains(response, 'Language')
        self.assertContains(response, 'I have a microphone')
        self.assertContains(response, '<h1><a href="/">Home</a><br></h1>')
        self.assertContains(response, '<textarea name="comment" maxlength="400" placeholder="Type in your comment ')
        self.assertContains(response, '<input type="submit" value="Post"/>')
