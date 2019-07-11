from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .models import Post, Thread

# Create your views here.

def index(request):
    # return all posts and first image found from each thread
    threads = Thread.objects.all()
    combined = dict()
    for t in threads:
        p = Post.objects.filter(thread__id=t.id).first()
        combined[t] = p
    return render(request, 'gallery.html', {'posts': combined})

def thread(request, id=None, slug=None):
    if slug:
        thread = get_object_or_404(Thread, slug=slug)
    if id:
        thread = get_object_or_404(Thread, pk=id)

    posts = Post.objects.filter(thread__id=thread.pk)
    return render(request, 'thread.html', {'thread': thread, 'posts': posts})
