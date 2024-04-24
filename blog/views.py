from django.shortcuts import render, get_object_or_404
from .models import Post
from django.views.generic import ListView
from .models import Post, Comment
from .forms import CommentForm

def post_list(request):
    # Retrieve all Post objects from the database
    posts = Post.objects.all()

    # Render the 'list.html' template and pass the retrieved posts to it
    return render(request, 'blog/post/list.html', {'posts': posts})
from django.shortcuts import render, get_object_or_404
from .models import Post

def post_detail(request, year, month, day, post):
    # Retrieve a specific Post object based on the year, month, day, and post slug
    post = get_object_or_404(Post,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)

    # Render the 'detail.html' template and pass the retrieved post to it
    return render(request, 'blog/post/detail.html', {'post': post})


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def post_list(request):
    object_list = Post.objects.all()
    paginator = Paginator(object_list, 3)  # 3 articole pe pagină

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:  # Returnează prima pagină când numărul paginii nu este un întreg
        posts = paginator.page(1)
    except EmptyPage:  # Dacă numărul paginii este mai mare decât numărul total al paginilor, returnăm ultima pagină
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/post/list.html', {'page': page, 'posts': posts})

class PostListView(ListView):
    queryset = Post.objects.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, publish__year=year, publish__month=month, publish__day=day)

    comments = post.comments.filter(active=True)
    new_comment = None
    comment_form = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, 'blog/post/detail.html', {
        'post': post,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form
    })