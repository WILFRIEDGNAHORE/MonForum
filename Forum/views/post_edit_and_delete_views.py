from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from ..models import Community, Post, Comment
from ..forms import PostCreateForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator






@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Vérifiez si l'utilisateur est l'auteur du post
    if post.author != request.user:
        messages.error(request, "Vous ne pouvez pas modifier ce post.")
        return redirect('post_list', community_id=post.community.id)

    if request.method == 'POST':
        form = PostCreateForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Le post a été modifié avec succès.")
            return redirect('post_detail', post_id=post.id)
    else:
        form = PostCreateForm(instance=post)

    return render(request, 'edit_post.html', {'form': form, 'post': post})







@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Vérifiez si l'utilisateur est l'auteur du post
    if post.author != request.user:
        messages.error(request, "Vous ne pouvez pas supprimer ce post.")
        return redirect('post_list', community_id=post.community.id)

    if request.method == 'POST':
        post.delete()
        messages.success(request, "Le post a été supprimé avec succès.")
        return redirect('post_list', community_id=post.community.id)

    return render(request, 'confirm_delete_post.html', {'post': post})

