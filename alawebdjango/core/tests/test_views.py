# coding=utf-8

from django.test import TestCase, Client
from django.core.urlresolvers import reverse


class IndexViewTestCase(TestCase):

    def setUp(self):
        self.response = self.client.get('/')

    def test_status_code(self):
        """ GET / must return status code 200 """
        self.assertEquals(self.response.status_code, 200)

    def test_template_used(self):
        """ Must use index.html """
        self.assertTemplateUsed(self.response, 'index.html')
