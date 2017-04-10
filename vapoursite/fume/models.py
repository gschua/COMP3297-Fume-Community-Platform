from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin

import os

#rename the filename and path to 'fume/static/fume/$attribute/$instance_id.ext'
def upload_path_handler(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (instance.pk, ext)
    return os.path.join('static', 'avatars', filename)
#-------------------------------------------------------------
#class MyUserManager(BaseUserManager):
#    def create_user(self, username, email, password=None):
#        user = self.model(
#            username=username,
#            email = MyUserManager.normalize_email(email),
#        )
#        user.set_password(password)
#        user.save(using=self._db)
#        return user
#
#    def create_superuser(self, username, email, password):
#        user = self.create_user(
#            username = email,
#            email = email,
#            password = password,
#        )
#        user.is_staff = True
#        user.save(using=self._db)

class Admin(models.Model):
    def __str__(self):
        return self.username
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)

class Publisher(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length=254)

class Genre(models.Model):
    def __str__(self):
        return self.text
    text = models.CharField(max_length=30)

class Platform(models.Model):
    def __str__(self):
        return self.text
    text = models.CharField(max_length=30)

class Game(models.Model):
    def __str__(self):
        return self.title
    title = models.CharField(max_length=254)
    price = models.FloatField(default=0.0)
    score = models.FloatField(default=0.0)
    description_short = models.TextField(max_length=500, null=True)
    description_long = models.TextField(null=True)
    release_date = models.DateField('Release Date', default=timezone.now)
    large_image = models.ImageField(upload_to=upload_path_handler)
    small_image = models.ImageField(upload_to=upload_path_handler)
    publisher = models.ForeignKey(Publisher, null=True)
    genre = models.ForeignKey(Genre, null=True)
    platform = models.ManyToManyField(Platform)
    featured = models.BooleanField(default=False)

class Member(AbstractBaseUser, PermissionsMixin):
    def __str__(self):
        return self.username
    objects=UserManager()
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=254)
    email = models.EmailField(unique=True)
    screen_name = models.CharField(max_length=30, default='Unnamed')
    avatar = models.ImageField(upload_to=upload_path_handler, null=True, blank=True)
    acc_spending = models.FloatField(default=0.0)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    #is_superuser = models.BooleanField(default=False)
    last_login = models.DateTimeField('Date/time of last login', null=True, blank=True)
    date_joined = models.DateTimeField('Date/time of registeration', default=timezone.now)
    REQUIRED_FIELDS = ['email']
    USERNAME_FIELD = 'username'
    PASSWORD_FIELD = 'password'
    EMAIL_FIELD = 'email'

    def get_short_name(self):
        return self.screen_name
    def get_full_name(self):
        return self.username



class Transaction(models.Model):
    def __str__(self):
        return self.purchase_datetime
    games = models.ForeignKey(Game, null=True)
    member = models.ForeignKey(Member, null=True)
    platform = models.ForeignKey(Platform, null=True)
    price = models.FloatField(default=0.0)
    rewards_used = models.IntegerField(default=0)
    is_purchased = models.BooleanField(default=False)
    purchase_datetime = models.DateTimeField('Date of Purchase', default=timezone.now)

class Tag(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length=254)
    #count = models.IntegerField(default=1)
    games = models.ManyToManyField(Game)

class MemberTag(models.Model):
    def __str__(self):
        return str(self.tag.name)+' by '+str(self.member.username)
    tag = models.ForeignKey(Tag, null=True)
    member =models.ForeignKey(Member, null=True)
    game = models.ForeignKey(Game, null=True)

class Review(models.Model):
    def __str__(self):
        return self.body
    body = models.TextField()
    score = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    member = models.ForeignKey(Member, null=True)
    game = models.ForeignKey(Game, null=True)

class Reward(models.Model):
    def __str__(self):
        return str(self.id)
    REWARD_STATUSES = (
        ('act', 'Active'),
        ('exp', 'Expired'),
        ('use', 'Used'),
    )
    award_date = models.DateField('Date of Awarding', default=timezone.now)
    expiry_date = models.DateField('Date of Expiry', default=timezone.now)
    status = models.CharField(max_length=3, choices=REWARD_STATUSES, default='act')
    member = models.ForeignKey(Member, null=True)
    transaction = models.ForeignKey(Transaction, null=True, blank=True)


#handling the uploaded filename
_UNSAVED_IMAGEFIELD = 'unsaved_imagefield'
@receiver(pre_save, sender=Member or Game)
def skip_saving_file(sender, instance, **kwargs):
    if not instance.pk and not hasattr(instance, _UNSAVED_IMAGEFIELD):
        if sender is Member:
            setattr(instance, _UNSAVED_IMAGEFIELD, instance.avatar)
            instance.avatar = None
        else:
            setattr(instance, _UNSAVED_IMAGEFIELD, instance.large_image)
            instance.large_image = None
            setattr(instance, _UNSAVED_IMAGEFIELD, instance.small_image)
            instance.small_image = None    
@receiver(post_save, sender=Member or Game)
def save_file(sender, instance, created, **kwargs):
    if created and hasattr(instance, _UNSAVED_IMAGEFIELD):
        if sender is Member:
            instance.avatar = getattr(instance, _UNSAVED_IMAGEFIELD)
            instance.save()
        else:
            instance.large_image = getattr(instance, _UNSAVED_IMAGEFIELD)
            instance.small_image = getattr(instance, _UNSAVED_IMAGEFIELD)
            instance.save() 

    