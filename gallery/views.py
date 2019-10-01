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
    form = PostForm()
    return render(request, 'board_view.html', {'board': board, 'threads': threads, 'form': form})

# Create new post on thread view.
def create_post(request, board=None, thread=None):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = Post()
            post.text       =   form.cleaned_data['text']
            post.thread     =   Thread.objects.get(pk=thread)
            post.thread.board = Board.objects.filter(name=board).first()
            post.original   =   request.FILES.get('original')
            post.user       =   request.user
            post.save()
            return HttpResponseRedirect('/' + board + '/' + str(thread))
    else:
        form = PostForm()
    
    return render(request, 'post_form.html', {'form': form})

# Create new thread on board view.
def create_thread(request, board=None):
    # Create new thread
    b = get_object_or_404(Board, name=board)
    thread = Thread()
    thread.board = b
    thread.save()
    return create_post(request, b.name, thread.pk)

# User actions on post.
def user_action(request, board=None, thread=None, post=None):
    if request.method == 'POST':
        if "delete" in request.POST:
            print("delete")
            p = Post.objects.get(pk=post)
            p.delete()

            # Post count in thread is 0, delete thread.
            t = Thread.objects.get(pk=thread)
            if not Post.objects.filter(thread=t.pk).count():
                t.delete()

        elif "update" in request.POST:
            print("update")
        elif "ban" in request.POST:
            print("ban")
        elif "move" in request.POST:
            print("move")
        else:
            print("User tried unknown action.")
    else:
        print("User tried unknown action.")
        
    return HttpResponseRedirect('/' + board + '/' + str(thread) + '#' + str(post))
