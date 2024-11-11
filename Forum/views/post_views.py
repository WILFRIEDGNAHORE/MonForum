from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from ..models import Community, Post, Comment
from ..forms import PostCreateForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

# Vue pour la création d'un post
@login_required
def create_post(request, community_id):
    community = get_object_or_404(Community, id=community_id)
    if request.method == 'POST':
        form = PostCreateForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.community = community
            post.save()
            messages.success(request, "Le post a été créé avec succès.")
            return redirect('post_list', community_id=community_id)
    else:
        form = PostCreateForm()
    return render(request, 'create_post.html', {'form': form, 'community': community})

# Vue pour afficher les détails d'un post
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post).order_by('-created_at')
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            messages.success(request, "Votre commentaire a été ajouté avec succès.")
            return redirect('post_detail', post_id=post.id)
    else:
        comment_form = CommentForm()
    return render(request, 'post_detail.html', {'post': post, 'comments': comments, 'comment_form': comment_form})

def all_post_list(request):
    posts = Post.objects.all().order_by('-created_at')  # Récupère tous les posts, triés par date de création

    # Pagination
    paginator = Paginator(posts, 10)  # 10 posts par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'all_post_list.html', {'page_obj': page_obj})


@login_required
def vote_up(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.vote_up()  # Incrémente le nombre de votes positifs
    return redirect('post_detail', post_id=post.id)

@login_required
def vote_down(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.vote_down()  # Incrémente le nombre de votes négatifs
    return redirect('post_detail', post_id=post.id)



