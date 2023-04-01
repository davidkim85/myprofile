from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from django.dispatch import receiver
from allauth.account.signals import user_signed_up


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset() \
            .filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    image = models.ImageField(upload_to='images/%Y/%m/%d/')
    url = models.URLField(max_length=2000)
    preArticle = models.TextField(blank=True)
    fullArticle = models.TextField(blank=True)
    blockquote = models.TextField(blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)
    published = PublishedManager()
    tags = TaggableManager()

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(default=None, max_length=255)
    email = models.CharField(default=None, max_length=500)
    picture = models.ImageField(default='default.jpg', upload_to='profile_pics', max_length=255)

    def __str__(self):
        return self.user.username

    @receiver(user_signed_up)
    def populate_profile(sociallogin, user, **kwargs):

        user.profile = Profile()

        if sociallogin.account.provider == 'facebook':
            user_data = user.socialaccount_set.filter(provider='facebook')[0].extra_data
            picture_url = "http://graph.facebook.com/" + sociallogin.account.uid + "/picture?type=large"
            email = user_data['email']
            full_name = user_data['name']

        if sociallogin.account.provider == 'google':
            user_data = user.socialaccount_set.filter(provider='google')[0].extra_data
            picture_url = user_data['picture']
            email = user_data['email']
            full_name = user_data['name']

        if sociallogin.account.provider == 'github':
            user_data = user.socialaccount_set.filter(provider='github')[0].extra_data
            picture_url = user_data['avatar_url']
            email = user_data['email']
            full_name = user_data['name']

        user.profile.picture = picture_url
        user.profile.email = email
        user.profile.full_name = full_name
        user.profile.save()


class CommentedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset() \
            .filter(active=True)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(Profile, models.SET_NULL, blank=True, null=True, related_name='authors')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    avatar = models.ImageField(default='default.jpg', upload_to='avatar_pics', max_length=255)
    commented = CommentedManager()

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['created']),
        ]

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'


class Visitor(models.Model):
    csrf = models.CharField(max_length=32)
    agent = models.CharField(max_length=255)
    visited = models.DateTimeField(auto_now_add=True)
    requests = models.BigIntegerField(default=0)
    visits=models.BigIntegerField(default=0)
    device = models.CharField(max_length=100,blank=True)
    ip = models.CharField(max_length=30,blank=True)
    os = models.CharField(max_length=30,blank=True)


    class Meta:
        ordering = ['-visited']
        indexes = [
            models.Index(fields=['visited']),
        ]
