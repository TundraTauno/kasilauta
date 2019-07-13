from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseNotFound

from .models import Post, Thread, Board

# Create your views here.

# Front page.
# example: /
def index(request):
    threads = Thread.objects.all()
    return render(request, 'main_view.html', {'threads': threads})

# Detailed view for thread.
# name  - board name
# id    - thread id
# example: /b/123
def thread_detail(request, name=None, id=None):
    if name:
        board = get_object_or_404(Board, name=name)
    if id:
        thread = get_object_or_404(Thread, pk=id)
    
    return render(request, 'thread_detail.html', {'thread': thread})

# Board view.
# name  - board name
# example: /b/
def board_view(request, name=None):
    # redirect to frontpage if board is not found
    if name:
        threads = Thread.objects.filter(board__name=name)
        if not threads:
            return HttpResponseNotFound
    return render(request, 'board_view.html', {'threads': threads})
