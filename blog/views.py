from django.shortcuts import render
from django.http import HttpResponse
from .models import BlogPost

# Create your views here.
def index(request):
    allblog=BlogPost.objects.all()
    print(len(allblog))
    return render(request,'blog/index.html',{'allblog':allblog})

def blogpost(request,id):
    allblog=BlogPost.objects.all()
    # post={'prev':'','current':'','next':''}
    post=[]
    prev=''
    next=''
    if(id>1):
        prev=BlogPost.objects.filter(post_id=id-1)[0]
    curr=BlogPost.objects.filter(post_id=id)[0]
    if id<len(allblog):
        next=BlogPost.objects.filter(post_id=id+1)[0]
    post.append([prev,curr,next])
    print("The value of post",prev.title)
    return render(request,'blog/blogPost.html',{'post':post})