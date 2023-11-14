from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from utils.notification_service import send_email
from .models import BlogPost


@receiver(post_save, sender=BlogPost)
def send_email_on_blog_post_create(sender, instance, created, **kwargs):
    try:
        if created:
            print("Sending email")
            subject = 'New Blog Post Created'
            to_email = instance.author.email
            html_message = '<h1>New Blog Post Created</h1>'
            send_email(subject, to_email, html_message)
    except:
        print("Error sending email")
