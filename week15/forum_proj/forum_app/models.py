from django.db import models
from datetime import datetime
# Create your models here.

# microblog_v3
from django.conf import settings
from django.contrib.auth.models import AbstractUser, UserManager, User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

class Articles(models.Model):
    """
    文章
    """
    articleid = models.CharField(
        max_length=30, verbose_name='文章id', default='')
    title = models.CharField(
        max_length=30, verbose_name='文章標題', default='')
    article = models.CharField(
        max_length=30, verbose_name='文章内容', default='')
    createtime = models.DateTimeField(auto_now_add=True)
    # 第一次migrations需注释掉owner
    owner = models.ForeignKey(
        'auth.User', related_name='articles', on_delete=models.CASCADE)

    class Meta:
        ordering = ['createtime']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):

        super(Articles, self).save(*args, **kwargs)

# https://docs.djangoproject.com/zh-hans/2.2/topics/auth/customizing/#extending-django-s-default-user

class UserProfile(models.Model):
    username = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    nickname = models.CharField(max_length=30, verbose_name='暱稱', default='')
    phone_number = models.CharField(max_length=20, verbose_name='手機', unique=True, blank=True)
    createtime = models.DateTimeField(auto_now_add=True, verbose_name='創建時間')
    description = models.CharField(max_length=30, verbose_name='個人簡介', default='')
    score = models.BigIntegerField(verbose_name='積分', default=0)

    # objects = UserManager()

    @classmethod
    def get_blacklist(cls):
        # seek that is_active = False
        return cls.objects.filter(is_active=False)

    class Meta:
        verbose_name = 'User Profile'
        # proxy = True
 

    # 當生成 user 的時候會自動生成 UserProfile
    # 原型是: receiver(signal, **kwargs), 當User產生post_save信號時
    @receiver(post_save, sender=User)  
    def handler_user_create_content(sender, instance, created, **kwargs):
        # 如果第一次創建
        if created:  
            # 綁定User實例到UserProfile的username字段
            UserProfile.objects.create(username=instance)  
        
    @receiver(post_save, sender=User)  
    def handler_user_save_content(sender, instance, created, **kwargs):
        # profile = UserProfile.objects.create(username=instance)
        # 保存UserProfile的内容 ,profile是username字段外键的related_name名
        instance.profile.save()  