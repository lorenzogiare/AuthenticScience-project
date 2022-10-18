from django.db import models
from django.conf import settings
from django.forms import BooleanField
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


# article status options 
STATUS_CHOICES = [
    ('D', 'draft'),
    ('P','Published'),
    ('W', 'Withdrawn'),
]

# article model
class Article(models.Model):

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=60)
    description = models.TextField(default='if you are curious read my content!', max_length=300)
    content = models.TextField()
    created_date = models.DateTimeField(default=timezone.now, editable=False)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='D')
    published_date = models.DateTimeField(blank=True, null=True)
    tx_id = models.CharField(null=True, blank=True, max_length=100)
    
    def publish(self):
        self.published_date = timezone.now()
        self.save()

# IP model, IP adresses are registered after every login (to warn about malevolent logins)
class IpAddress(models.Model):
    login_date = models.DateTimeField('time of login')
    ip_address = models. GenericIPAddressField()
    user_logged = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    country = models.CharField(max_length=20)

# this model represents requests sent by users in order to get an articles's data and transaction info
class ArticleDetailsRequest(models.Model):
    user = models.CharField(max_length=20)
    title_requested = models.CharField(max_length=100)
    id_string = models.CharField(max_length=10)
    pk_requested = models.IntegerField(default=0)


#-----EXSTENSION-OF-THE-USER-MODEL----------------------------------------------------
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    verified_author = models.BooleanField(default=False)

#when a new User object is created, the Profile model is too
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()