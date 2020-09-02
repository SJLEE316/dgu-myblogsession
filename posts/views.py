from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth.decorators import login_required

def new(request):
    return render(request, 'posts/new.html')

def create(request):
    if request.method == "POST":
        title=request.POST.get('title')
        content=request.POST.get('content')
        image=request.FILES.get('image')
        user = request.user
        Post.objects.create(title=title, content=content, image=image, user=user)
    return redirect('posts:main')

def main(request):
    posts = Post.objects.all()
    return render(request, 'posts/main.html', {'posts': posts})

def show(request, id):
    post = Post.objects.get(pk=id)
    post.view_count += 1
    post.save()
    all_comments = post.comments.all().order_by('-created_at')
    return render(request, 'posts/show.html', {'post': post, 'comments':all_comments})

def update(request, id):
    post=get_object_or_404(Post,pk=id)
    if request.method=="POST":
        post.title=request.POST['title']    
        post.content=request.POST['content']
        post.image=request.FILES.get('image')
        post.save()
        return redirect('posts:show',post.id)
    return render(request, 'posts/update.html', {"post":post})    

def delete(request, id):
    post = get_object_or_404(Post, pk=id)
    post.delete()
    return redirect('posts:main')

def create_comment(request, post_id) : #어느 게시글?
    if request.method == "POST":
        post = get_object_or_404(Post, pk=post_id)
        current_user = request.user
        comment_content = request.POST.get('content') #textarea
        Comment.objects.create(content=comment_content, writer=current_user, post=post) #모델=우리가 넣어줄 값
    return redirect('posts:show', post.pk) #POST가 아니어도 return가능

@login_required
def post_like(request, post_id): #어떤 포스트?
    post = get_object_or_404(Post, pk=post_id)
    post_like, post_like_created = post.like_set.get_or_create(user=request.user)

    # if request.user in post.like_user_set.all(): #user가 안에 있으면
    #     post.like_user_set.remove(request.user)
    # else:
    #     post.like_user_set.add(request.user)

    if not post_like_created:
        post_like.delete()

    if request.GET.get('redirect_to') == 'show':
        return redirect('posts:show', post_id)
    else:
        return redirect('posts:main')

@login_required
def like_list(request):
    likes = request.user.like_set.all()
    return render(request,'posts/like_list.html',{'likes':likes})

# Create your views here.
