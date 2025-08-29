from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from ..models import PortFolio, Contact
from .tests_settings import MediaCleanTestCase


User = get_user_model()


class HomeViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="11", about="test")

    def test_view(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

        user_in_context = response.context["user"]
        self.assertEqual(user_in_context.about, self.user.about)


class ContactViewTests(MediaCleanTestCase):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(username="testuser", password="11", about="test")
        Contact.objects.filter(user=self.user).update(phone="38012345")
        self.contact = Contact.objects.get(user=self.user)
        
        self.photo_content = (
            b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01'
            b'\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89'
            b'\x00\x00\x00\nIDATx\xdacd\xf8\x0f\x00\x01\x05\x01\x02'
            b'\xa2\xdd\xba\x0b\x00\x00\x00\x00IEND\xaeB`\x82'
        )
        self.photo_file = SimpleUploadedFile(
            "test_photo.png", self.photo_content, content_type="image/png"
        )

    def test_view(self):
        response = self.client.get("/contact/")
        self.assertEqual(response.status_code, 200)

        contact_in_context = response.context["contact"]
        self.assertEqual(contact_in_context.phone, self.contact.phone)

    def test_post(self):
        response = self.client.post("/contact/", {
            "phone": "973283",
            "file": self.photo_file,
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("success", response.context)


class PortfolioViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="11", about="test")
        self.portfolio = PortFolio.objects.create(user=self.user, name="1")

    def test_view(self):
        response = self.client.get("/portfolio/")
        self.assertEqual(response.status_code, 200)

        portfolio_in_context = response.context["projects"]
        self.assertEqual(portfolio_in_context.last().name, self.portfolio.name)