from django.db import models
from django.contrib.auth.models import AbstractUser

from . import constants


class CustomerUser(AbstractUser):
    """
    Custom user model for attaching site owner data.

    Has fields:
    - photo: photo of the author of the site (optional)
    - about: about the author of the site (optional)
    - created_at: automatically create model creation time
    - inherited fields:
      - username
      - first_name
      - last_name
      - email
      - others...

    Has model connections with:
    - PortFolio: meny-to-one relationship
    - Contact: one-to-one connection

    Methods:
    - __str__: returns the full username or username
    - save: added instantiation of Contact models to standard behavior
    """
    photo = models.ImageField(upload_to="photos/user/", blank=True, verbose_name=constants.VERBOSE_PHOTO)
    about = models.TextField(blank=True, verbose_name=constants.VERBOSE_ABOUT)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=constants.VERBOSE_CREATED_AT)

    class Meta: 
        ordering = ["-created_at"]
        verbose_name = constants.VERBOSE_NAME_CUSTOMER_USER
        verbose_name_plural = constants.VERBOSE_NAME_CUSTOMER_USER_PLURAL

    def __str__(self):
        return self.get_full_name() or self.username
    
    def save(self, *args, **kwargs):
        new = self.id is None
        super().save(*args, **kwargs)

        if new:
            Contact.objects.create(user=self)

        
class PortFolio(models.Model):
    """
    Model for a collection of works for an author's portfolio.

    Has fields:
    - user: meny-to-one relationship with model CustomerUser
    - github: a link to the project's GitHub
    - photo: project photo (optional)
    - created_at: automatically create model creation time

    Method __str__: returns project name or username.
    """
    user = models.ForeignKey(
        to=CustomerUser, on_delete=models.CASCADE, related_name=constants.RELATED_NAME_PORTFOLIO, 
        verbose_name=constants.VERBOSE_NAME_PORTFOLIO
        )
    name = models.CharField(max_length=150, blank=True, verbose_name=constants.VERBOSE_NAME)
    github = models.URLField(blank=True, verbose_name=constants.VERBOSE_GITHUB)
    url = models.URLField(blank=True, verbose_name=constants.VERBOSE_URL)
    photo = models.ImageField(upload_to="photos/portgolio/", blank=True, null=True, verbose_name=constants.VERBOSE_PHOTO)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=constants.VERBOSE_CREATED_AT)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = constants.VERBOSE_NAME_PORTFOLIO
        verbose_name_plural =constants.VERBOSE_NAME_PORTFOLIO_PLURAL

    def __str__(self):
        return self.name or self.user.username


class Contact(models.Model):
    """
    Model for contacts of the CustomerUser model.

    Has fields:
    - user: one-to-one connection with model CustomerUser
    - phone: character string maximum characters 16 (optional)
    - telegram: url for telegram contact (optional)
    - linkedin: url for linkedin contact (optional)
    - github: link to the website author's GitHub (optional)
    - address: address of the site author (optional)
    - created_at: automatically create model creation time

    Method __str__: returns the full username or username.
    """
    user = models.OneToOneField(
        to=CustomerUser, on_delete=models.CASCADE, related_name=constants.VERBOSE_NAME_CONTACT,
        verbose_name=constants.RELATED_NAME_CONTACT
        )
    phone = models.CharField(max_length=16, blank=True, verbose_name=constants.VERBOSE_PHONE)
    telegram = models.URLField(blank=True, verbose_name=constants.VERBOSE_TELEGRAM)
    linkedin = models.URLField(blank=True, verbose_name=constants.VERBOSE_LINKEDIN)
    github = models.URLField(blank=True, verbose_name=constants.VERBOSE_GITHUB)
    address = models.TextField(blank=True, verbose_name=constants.VERBOSE_ADDRESS)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=constants.VERBOSE_CREATED_AT)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = constants.VERBOSE_NAME_CONTACT
        verbose_name_plural = constants.VERBOSE_NAME_CONTACT_PLURAL

    def __str__(self):
        return self.user.get_full_name() or self.user.username