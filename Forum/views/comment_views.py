from django.shortcuts import render, redirect, get_object_or_404
from ..models import Comment, Post
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..forms import CommentForm

# Vue pour ajouter un commentaire
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = CommentForm()
    return render(request, 'add_comment.html', {'form': form, 'post': post})



@login_required
def vote_up_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.vote_up()  # Incrémente le nombre de votes positifs
    return redirect('post_detail', post_id=comment.post.id)
# Vue pour voter sur un post ou un commentaire
@login_required
def vote(request, model, object_id, vote_type):
    if request.method == 'POST':
        # On récupère l'objet (post ou commentaire)
        if model == 'post':
            obj = get_object_or_404(Post, id=object_id)
        elif model == 'comment':
            obj = get_object_or_404(Comment, id=object_id)
        else:
            messages.error(request, "Modèle inconnu.")
            return redirect('community_list')

        # On applique le vote
        if vote_type == 'upvote':
            if model == 'post':
                obj.upvotes += 1
            elif model == 'comment':
                obj.upvotes += 1
        elif vote_type == 'downvote':
            if model == 'post':
                obj.downvotes += 1
            elif model == 'comment':
                obj.downvotes += 1
        obj.save()

        # Message de succès
        messages.success(request, f"Votre {vote_type} a été pris en compte.")
        return redirect('post_detail', post_id=obj.id if model == 'post' else obj.post.id)

    return redirect('community_list')

@login_required
def reply_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    post = comment.post

    if request.method == 'POST':
        content = request.POST.get('content')
        reply = Comment.objects.create(
            post=post,
            user=request.user,
            content=content,
            parent=comment
        )
        return redirect('post_detail', post_id=post.id)
@login_required
def vote_down_comment(request, comment_id):
    # Récupère le commentaire à partir de l'ID
    comment = get_object_or_404(Comment, id=comment_id)
    
    # Appelle la méthode pour voter négativement (décrémenter le nombre de votes négatifs)
    comment.vote_down()
    
    # Redirige l'utilisateur vers la page de détails du post
    return redirect('post_detail', post_id=comment.post.id)


