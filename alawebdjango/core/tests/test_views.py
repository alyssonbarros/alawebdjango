# coding=utf-8

from django.core.urlresolvers import reverse
from alawebdjango.core.forms import ContactForm
from django.test import TestCase
from django.core import mail



class IndexViewTestCase(TestCase):

    def setUp(self):
        self.resp = self.client.get('/contato/')
        self.url = reverse('index')

    def tearDown(self):
        pass

    def test_status_code(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)

    def test_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'index.html')

    def test_html(self):
        """Html must contain tags"""
        self.assertContains(self.resp,'<form')
        self.assertContains(self.resp,'<input', 3)
        self.assertContains(self.resp,'type="text"', 1)
        self.assertContains(self.resp,'type="email"')
        self.assertContains(self.resp,'type="submit"')

    def test_csrf(self):
        """Html must contain csrf """
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """Context must have contact form """
        form = self.resp.context['form']
        self.assertIsInstance(form, ContactForm)

    def test_form_has_fields(self):
        """Form must have 4 fields"""
        form = self.resp.context['form']
        self.assertSequenceEqual(['name', 'email', 'message'], list(form.fields))

class ContactPostTest(TestCase):
    def setUp(self):
        data = dict(name='Alysson Barros', email='alysson@barros.net',
                    message='Tenho interesse nos cursos da AlaWeb')

        self.resp = self.client.post('/contato/', data)

    def test_post(self):
        """Valid POST should redirect to /contato/"""
        self.assertEqual(302, self.resp.status_code)

    def test_send_contact_email(self):
        self.assertEqual(1, len(mail.outbox))

    def test_contact_email_subject(self):
        email = mail.outbox[0]
        expect = 'Confirmação de contato'

        self.assertEqual(expect, email.subject)

    def test_contact_email_from(self):
        email = mail.outbox[0]
        expect = 'arbarros372@gmail.com'

        self.assertEqual(expect, email.from_email)

    def test_contact_email_to(self):
        email = mail.outbox[0]
        expect = ['arbarros372@gmail.com', 'alysson@barros.net']

        self.assertEqual(expect, email.to)

    def test_contact_email_body(self):
        email = mail.outbox[0]

        self.assertIn('Alysson Barros', email.body)
        self.assertIn('alysson@barros.net', email.body)
        self.assertIn('Tenho interesse nos cursos da AlaWeb', email.body)

class ContactInvalidPost(TestCase):
    def setUp(self):
        self.resp = self.client.post('/contato/', {})

    def test_post(self):
        """Invalid POST shoud not redirect"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp,'contact.html')

    def test_has_form(self):
        form = self.resp.context['form']
        self.assertIsInstance(form, ContactForm)

    def test_form_has_errors(self):
        form = self.resp.context['form']
        self.assertTrue(form.errors)

class ContactSuccessMessage(TestCase):
    def test_message(self):
        data = dict(name='Alysson Barros', email='alysson@barros.net',
                    message='Tenho interesse nos cursos da AlaWeb')

        response = self.client.post('/contato/', data, follow=True)
        self.assertContains(response, 'Contato realizado com sucesso!')

