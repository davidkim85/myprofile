from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from blog.forms import CommentForm, EmailPostForm
from blog.models import Post, Comment, Profile
from taggit.models import Tag


def home(request):
    posts = Post.published.all()[:3]
    sent = False
    form = EmailPostForm(request.POST)
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            subject = cd['subject']
            message = cd['body']
            email = list()
            email.append(cd['email'])
            send_mail(subject, message, 'poramok@gmail.com', email)
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/home.html', {'posts': posts, 'form': form, 'sent': sent})


def post(request, year, month, day, post):
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    comments = Comment.commented.filter(post=post)
    form = CommentForm()
    paginator = Paginator(comments, 5)
    page_number = request.GET.get('page', 1)
    try:
        comments = paginator.page(page_number)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)
    comments = paginator.page(page_number)
    return render(request, 'blog/posts/post.html', {'post': post, 'comments': comments, 'form': form})


def search(request):
    keyword = request.GET['keyword']
    posts = Post.published.filter(title__icontains=keyword)
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    posts = paginator.page(page_number)
    return render(request, 'blog/posts/search.html', {'posts': posts})


def post_list(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = Post.published.filter(tags__in=[tag])
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/posts/list.html', {'posts': posts, 'tag': tag})


@require_POST
def post_comment(request, post_id, user_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    author = get_object_or_404(Profile, user_id=user_id)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = author
        comment.avatar = author.picture
        comment.save()
        return redirect(post.get_absolute_url())
    return redirect(post.get_absolute_url())
