from django.shortcuts import render,get_object_or_404,redirect
from .forms import PostForm,CommentForm
from .models import Post,Comment
from users.models import Profile
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
# Create your views here.
@login_required
def index(request):
   posts = Post.objects.filter(user=request.user)
   return render(request,'posts/index.html',{"posts":posts})



@login_required
def create_post(request):
    if request.method =="POST":
        form = PostForm(request.POST,files=request.FILES)
        if  form.is_valid():
           user_post= form.save(commit=False)
           user_post.user = request.user
           form.save()
    else:
       form = PostForm()
    return render(request,"posts/post.html",{'form':form})
@login_required
def feed(request):
   if request.method =="POST":
      post_id = request.POST.get('post_id')
      post = get_object_or_404(Post,id=post_id)
      comment_form = CommentForm(request.POST)
      new_comment = comment_form.save(commit=False)
      new_comment.post = post
      comment_form.save()
   else:
        comment_form = CommentForm() 
   posts = Post.objects.all()
   logged_user = request.user
   return render(request,'posts/all_posts.html',{"posts":posts,"logged_user":logged_user,'comment_form':comment_form})


def like_post(request):
   post_id = request.POST.get('post_id')
   post = get_object_or_404(Post,id=post_id)
   if post.liked_by.filter(id=request.user.id).exists():
      post.liked_by.remove(request.user)    
   else:
      post.liked_by.add(request.user)
   return redirect("feed")
  
