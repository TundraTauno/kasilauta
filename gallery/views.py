from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect

from .models import Post, Thread, Board
from .forms import PostForm

# Create your views here.

# Front page.
# example: /
def index(request):
    threads = Thread.objects.all()
    boards = Board.objects.all()
    return render(request, 'main_view.html', {'threads': threads, 'boards': boards})

# Detailed view for thread.
# name  - board name
# id    - thread id
# example: /b/123
def thread_detail(request, name=None, id=None):
    board = get_object_or_404(Board, name=name)
    thread = get_object_or_404(Thread, pk=id)
    form = PostForm()
    return render(request, 'thread_detail.html', {'thread': thread, 'form': form})

# Board view.
# name  - board name
# example: /b/
def board_view(request, name=None):
    board = get_object_or_404(Board, name=name)
    threads = Thread.objects.filter(board__name=name)
    return render(request, 'board_view.html', {'threads': threads})

# Create new post.
def create_post(request, board=None, id=None):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = Post()
            post.text       =   form.cleaned_data['text']
            post.thread     =   Thread.objects.get(pk=id)
            post.thread.board = Board.objects.filter(name=board).first()
            post.original   =   request.FILES.get('original')
            post.user       =   request.user
            post.save()
#             messages.success(request, "Thank you! You have successfully posted your picture!")
            return HttpResponseRedirect('/' + board + '/' + str(id))
    else:
        form = PostForm()
        
    return render(request, 'post_form.html', {'form': form})

