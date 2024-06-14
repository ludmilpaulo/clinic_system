from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()
from django.utils import timezone

from django_ckeditor_5.fields import CKEditor5Field

class Image(models.Model):
    image = models.ImageField(max_length=3000, default='', blank=True, upload_to='carousel_images/')

    def __str__(self):
        return self.image.name if self.image else ''


class Carousel(models.Model):
	image = models.ManyToManyField(Image)
	title = models.CharField(max_length=150)
	sub_title = models.CharField(max_length=100)

	def __str__(self):
		return self.title


# Create your models here.

class AboutUs(models.Model):
    title = models.CharField(max_length = 50)
    logo = models.ImageField(upload_to="logo/", blank=True, null=True)
    backgroundImage = models.ImageField(upload_to="Back_logo/", blank=True, null=True)
    backgroundApp = models.ImageField(upload_to="Back_logo/", blank=True, null=True)
    about = CKEditor5Field('Text', config_name='extends')
    born_date = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    # Social Network
    github = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)


    class Meta:
        verbose_name = 'about us '
        verbose_name_plural = 'about us '

    def __str__(self):
        return self.title


class Why_Choose_Us(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()

    class Meta:
        verbose_name = 'why choose us '
        verbose_name_plural = 'why choose us '

    def __str__(self):
        return self.title


class Team(models.Model):
    name = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    bio = models.CharField(max_length=500)
    image = models.ImageField(upload_to='chef/')
    github = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)

    class Meta:
        verbose_name = 'Squad'
        verbose_name_plural = 'Squad'

    def __str__(self):
        return self.name





class Chat(models.Model):
   # order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='chat_messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
    
    
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
import logging

class Contact(models.Model):
    subject = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    message = models.TextField(verbose_name='Conteúdo')
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Client contact'
        verbose_name_plural = 'Client contacts'

    def __str__(self):
        return self.subject

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Contact)
def send_confirmation_email(sender, instance, created, **kwargs):
    if created:
        subject = "Thank you for contacting Men's Clinic"
        logo_url = f"{settings.ALLOWED_HOSTS[0]}/media/logo/logo2.png"
        message = render_to_string('contact_confirmation_email.html', {
            'subject': instance.subject,
            'message': instance.message,
            'logo_url': logo_url
        })
        logger.info("Attempting to send email to %s", instance.email)
        try:
            send_mail(
                subject,
                '',  # Plain text message
                settings.EMAIL_HOST_USER,
                [instance.email],
                fail_silently=False,
                html_message=message
            )
            logger.info("Email sent successfully to %s", instance.email)
        except Exception as e:
            logger.error("Error sending email: %s", e)
