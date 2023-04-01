from django import template
from django.db.models import Sum

from blog.models import Post, Comment, Profile, Visitor

register = template.Library()


@register.inclusion_tag('blog/posts/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


@register.inclusion_tag('blog/posts/tags.html')
def show_tags():
    tags = Post.tags.all()
    return {'tags': tags}


@register.simple_tag
def total_comments(post):
    return Comment.commented.filter(post=post).count()


@register.simple_tag
def total_posts():
    return Post.published.count()


@register.simple_tag
def total_visitors():
    return Profile.objects.count()


@register.simple_tag
def total_all_comments():
    return Comment.commented.count()


@register.simple_tag
def total_visitors():
    return Visitor.objects.count()


@register.simple_tag
def total_requests():
    pubs = Visitor.objects.aggregate(Sum("requests"))
    return pubs['requests__sum']




