from django.views.generic import TemplateView
from blog.models import Post, Comment
from blog.forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.

class AboutView(TemplateView):
    template_name = 'blog/about.html'


def PostList(request):
    post_list = Post.objects.all().filter(publish_date__isnull=False).order_by('-publish_date')
    page = request.GET.get('page', 1)

    paginator = Paginator(post_list, 5)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post_list.html', locals())


@login_required
def PostCreate(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.author = request.user
            form.save()
            post = Post.objects.filter(author=request.user).order_by('-id')
            post = post.first()
            return redirect('post_detail', post.id)
    return render(request, 'blog/post_form.html', locals())


@login_required
def PostUpdate(request, pk):
    obj = Post.objects.get(id=pk)
    form = PostForm(instance=obj)
    if request.method == 'POST':
        form = PostForm(data=request.POST, files=request.FILES, instance=obj)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.author = request.user
            obj.save()
            return redirect('post_detail', pk)
    return render(request, 'blog/post_form.html', locals())


@login_required
def PostDelete(request, pk):
    obj = get_object_or_404(Post, pk=pk)
    post_pk = obj.pk
    if obj.author == request.user:
        obj.delete()
    return redirect('post_list')


@login_required
def DraftView(request):
    post_list = Post.objects.filter(author=request.user).filter(publish_date__isnull=True).order_by('-publish_date')

    user_list = User.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(post_list, 10)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post_list.html', locals())


@login_required(login_url='accounts/login')
def add_comments_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_list')
    form = CommentForm()
    return render(request, 'blog/comment_form.html', locals())


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    if comment.author == request.user:
        post_pk = comment.post.pk
        comment.delete()
    return redirect('post_detail', post_pk)


@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk)
