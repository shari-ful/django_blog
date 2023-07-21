from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Blog, Topic, Comment
from .forms import CreateBlog

# Create your views here.



def home(request):

    q = request.GET.get('q') if request.GET.get('q') != None else ''

    blogs = Blog.objects.filter(
        Q(topic__name__icontains=q)|
        Q(title__icontains=q)|
        Q(description__icontains=q)
        )
    
    topics = Topic.objects.all()

    blog_count = blogs.count()

    comments = Comment.objects.all()

    context={'blogs':blogs, 'topics': topics, 'blog_count': blog_count, 'comments':comments}

    return render(request, 'home.html', context=context)

def blog_items(request, pk):

    blog = Blog.objects.get(id=pk)

    comments = blog.comment_set.all().order_by('-created_at')
    participants = blog.participants.all()

    if request.method == 'POST':
        comment = Comment.objects.create(
            user = request.user,
            blog = blog,
            comment = request.POST.get('comment')
        )
        blog.participants.add(request.user)

        return redirect('blogitem', pk=blog.id)

    context={'blog':blog, 'comments':comments, 'participants':participants}

    return render(request, 'itemblog.html', context=context)

@login_required(login_url='login')
def create_blog(request):

    form = CreateBlog()
    topics = Topic.objects.all()

    if request.method == 'POST':
        form = CreateBlog(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context={'form':form, 'topics': topics}

    return render(request, 'createblog.html', context=context)

@login_required(login_url='login')
def update_blog(request, pk):
    blog = Blog.objects.get(id=pk)
    form = CreateBlog(instance=blog)
    topics = Topic.objects.all()

    if request.user != blog.host:
        return HttpResponse('You are not allowd to Update this blog')

    if request.method == 'POST':
        form = CreateBlog(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('home')
        
    context = {'form': form, 'topics':topics}
    return render(request, 'createblog.html', context=context)

@login_required(login_url='login')
def delete_blog(request, pk):
    blog = Blog.objects.get(id=pk)

    if request.user != blog.host:
        return HttpResponse("You aren't Eligible to delete the Blog")

    if request.method == 'POST':
        blog.delete()
        return redirect('home')
        
    context = {'obj': blog}
    return render(request, 'delete.html', context=context)


def login_page(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User(username=username, password=password)
        except:
            messages.error(request, 'Username not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        
        else:
            messages.error(request, 'Incorreect Username or Password')
        
    context = {'page':page}
    return render(request, 'auth.html', context=context)


def logout_page(request):
    logout(request)
    return redirect('home')


def register_page(request):
    page = 'register'

    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        
        else:
            messages.error(request, 'An error Accured')

    context = {'form':form, 'page':page}
    return render(request, 'auth.html', context=context)


@login_required(login_url='login')
def delete_comment(request, pk):
    comment = Comment.objects.get(id=pk)

    if request.user != comment.user:
        return HttpResponse("You aren't Eligible to delete the Comment")

    if request.method == 'POST':
        comment.delete()
        return redirect('blogitem')
        
    context = {'obj': comment}
    return render(request, 'delete.html', context=context)


def user_profile(request, pk):
    user = User.objects.get(id=pk)
    blogs = user.blog_set.all()
    comments = user.comment_set.all()
    topics = Topic.objects.all()
    context = {'user':user, 'blogs': blogs, 'comments':comments, 'topics':topics}
    return render(request, 'profile.html', context=context)
