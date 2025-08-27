from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from ..models import PortFolio, Contact, CustomerUser


class CustomerUserModelTests(TestCase):
    def setUp(self):
        photo_content = (
            b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01'
            b'\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89'
            b'\x00\x00\x00\nIDATx\xdacd\xf8\x0f\x00\x01\x05\x01\x02'
            b'\xa2\xdd\xba\x0b\x00\x00\x00\x00IEND\xaeB`\x82'
        )
        self.photo_file = SimpleUploadedFile(
            "test_photo.png", photo_content, content_type="image/png"
        )

        self.valid_data = {
            "photo": self.photo_file,
            "about": "This is test about",
            "username": "testusername",
            }
        
        self.user = CustomerUser.objects.create_user(**self.valid_data, password="11")

    def test_create(self):
        self.assertTrue(self.user.photo.name.endswith(".png"), msg=f"The image or photo field address is not saved correctly. {self.user.photo.name}")

        valid_data = self.valid_data.copy()
        del valid_data["photo"]

        for key, value in valid_data.items():
            self.assertEqual(getattr(self.user, key), value,
                msg=f'field:"{key}" value:"{getattr(self.user, key)}" does not match the value it was created from:"{value}"')

    def test_partial_create(self):
        valid_data = self.valid_data.copy()
        del valid_data["photo"]
        valid_data["username"] = "user2"
        
        user = CustomerUser.objects.create_user(**valid_data, password="22")

        for key, value in valid_data.items():
            self.assertEqual(getattr(user, key), value,
                msg=f'field:"{key}" value:"{getattr(user, key)}" does not match the value it was created from:"{value}"')

    def test_str_method(self):
        self.assertEqual(str(self.user), self.user.username, msg=f'alternative str not correct "{str(self.user)}" not "{self.user.username}"')

        user = CustomerUser.objects.create_user(first_name="Test", last_name="Tes", username="user2", password="22")
        self.assertEqual(str(user), user.get_full_name(), msg=f'not correct str "{str(user)}" no "{user.get_full_name()}"')


class PortFolioModelTests(TestCase):
    def setUp(self):
        photo_content = (
            b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01'
            b'\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89'
            b'\x00\x00\x00\nIDATx\xdacd\xf8\x0f\x00\x01\x05\x01\x02'
            b'\xa2\xdd\xba\x0b\x00\x00\x00\x00IEND\xaeB`\x82'
        )
        self.photo_file = SimpleUploadedFile(
            "test_photo.png", photo_content, content_type="image/png"
        )
        self.user = CustomerUser.objects.create_user(username="testusername", password="11")

        self.valid_data = {
            "user": self.user,
            "name": "Test project",
            "github": "https://translate.google.com.ua/",
            "url": "https://translate.google.com.ua/",
            "photo": self.photo_file,
        }
        self.portfolio = PortFolio.objects.create(**self.valid_data)

    def test_create(self):
        self.assertTrue(self.portfolio.photo.name.endswith(".png"), msg=f"The image or photo field address is not saved correctly. {self.portfolio.photo.name}")

        valid_data = self.valid_data.copy()
        del valid_data["photo"]

        for key, value in valid_data.items():
            self.assertEqual(getattr(self.portfolio, key), value,
                msg=f'field:"{key}" value:"{getattr(self.portfolio, key)}" does not match the value it was created from:"{value}"')

    def test_partial_create(self):
        valid_data = self.valid_data.copy()
        del valid_data["photo"]
        del valid_data["name"]
        portfolio = PortFolio.objects.create(**valid_data)

        for key, value in valid_data.items():
            self.assertEqual(getattr(portfolio, key), value,
                msg=f'field:"{key}" value:"{getattr(portfolio, key)}" does not match the value it was created from:"{value}"')

    def test_str_method(self): 
        self.assertEqual(str(self.portfolio), self.valid_data["name"], msg=f'not correct str "{str(self.portfolio)}" no "{self.valid_data["name"]}"')

        valid_data = self.valid_data.copy()
        del valid_data["name"]
        portfolio = PortFolio.objects.create(**valid_data)
        self.assertEqual(str(portfolio), self.user.username, msg=f'alternative str not correct "{str(portfolio)}" not "{self.user.username}"')


class ContactModelTests(TestCase):
    def setUp(self):
        self.user = CustomerUser.objects.create_user(username="testusername", password="11")
        self.user2 = CustomerUser.objects.create_user(first_name="Test", last_name="Name",  username="testusername2", password="22")
        self.valid_data = {
            "telegram": "https://translate.google.com.ua/",
            "linkedin": "https://translate.google.com.ua/",
            "github": "https://translate.google.com.ua/",
            "address": "https://translate.google.com.ua/",
        }
        self.valid_data2 = {
            "telegram": "https://translate.google.com.ua/",
            "address": "https://translate.google.com.ua/",
        }
        Contact.objects.filter(user=self.user).update(**self.valid_data)
        self.contact = Contact.objects.get(user=self.user)
        Contact.objects.filter(user=self.user2).update(**self.valid_data2)
        self.contact2 = Contact.objects.get(user=self.user2)

    def test_create(self):
        for key, value in self.valid_data.items():
            self.assertEqual(getattr(self.contact, key), value,
                msg=f'field:"{key}" value:"{getattr(self.contact, key)}" does not match the value it was created from:"{value}"')

    def test_partial_create(self):
        for key, value in self.valid_data2.items():
            self.assertEqual(getattr(self.contact2, key), value,
                msg=f'field:"{key}" value:"{getattr(self.contact2, key)}" does not match the value it was created from:"{value}"')

    def test_str_method(self): 
        self.assertEqual(str(self.contact), self.user.username, msg=f'alternative str not correct "{str(self.contact)}" not "{self.user.username}"')
        self.assertEqual(str(self.contact2), self.user2.get_full_name(), msg=f'not correct str "{str(self.contact2)}" no "{self.user2.get_full_name()}"')