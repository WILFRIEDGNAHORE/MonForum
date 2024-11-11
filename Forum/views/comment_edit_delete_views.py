from django.shortcuts import render, redirect, get_object_or_404
from ..models import Comment, Post
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..forms import CommentForm

@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    # Vérifiez si l'utilisateur est l'auteur du commentaire
    if comment.user != request.user:
        messages.error(request, "Vous ne pouvez pas modifier ce commentaire.")
        return redirect('post_detail', post_id=comment.post.id)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, "Le commentaire a été modifié avec succès.")
            return redirect('post_detail', post_id=comment.post.id)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'edit_comment.html', {'form': form, 'comment': comment})
@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    # Vérifiez si l'utilisateur est l'auteur du commentaire
    if comment.user != request.user:
        messages.error(request, "Vous ne pouvez pas supprimer ce commentaire.")
        return redirect('post_detail', post_id=comment.post.id)

    if request.method == 'POST':
        comment.delete()
        messages.success(request, "Le commentaire a été supprimé avec succès.")
        return redirect('post_list', post_id=comment.post.id)

    return render(request, 'confirm_delete_comment.html', {'comment': comment})
