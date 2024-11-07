from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout

from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm, PostCreateForm, CommentForm, VoteForm
from .models import Community, Post, Comment, Notification
from django.contrib.auth.decorators import login_required


# Vue pour l'inscription
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Votre compte a été créé avec succès !")
            return redirect('community_list')
        else:
            messages.error(request, "Erreur lors de l'inscription. Veuillez vérifier vos informations.")
    else:
        form = UserRegisterForm()

    return render(request, 'register.html', {'form': form})

# Vue pour la connexion
def login_view(request):
    if request.method == 'POST':
        # Récupérer les données du formulaire
        username = request.POST['username']
        password = request.POST['password']

        # Vérifier si l'utilisateur existe dans la base de données
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None

        # Authentification de l'utilisateur
        if user is not None:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # Connexion de l'utilisateur si l'authentification est réussie
                login(request, user)
                return redirect('community_list')  # Redirige vers la page d'accueil après la connexion
            else:
                # Si l'authentification échoue, afficher un message d'erreur
                messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
        else:
            messages.error(request, "Cet utilisateur n'existe pas.")

    # Si la requête est en GET ou si le formulaire est vide, on affiche le formulaire
    return render(request, 'login.html')


        
        
        

# Vue pour la déconnexion
def user_logout(request):
    logout(request)
    messages.info(request, "Vous êtes maintenant déconnecté.")
    return redirect('login')

# Vue pour la liste des communautés
def community_list(request):
    communities = Community.objects.all()
    return render(request, 'community_list.html', {'communities': communities})

# Vue pour afficher les posts d'une communauté
def post_list(request, community_id):
    community = get_object_or_404(Community, id=community_id)
    posts = Post.objects.filter(community=community).order_by('-created_at')
    
    # Pagination
    paginator = Paginator(posts, 10)  # 10 posts par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'post_list.html', {'community': community, 'page_obj': page_obj})


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

# Vue pour la création d'un post
@login_required
def create_post(request, community_id):
    community = Community.objects.get(id=community_id)

    if request.method == 'POST':
        form = PostCreateForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # Définir l'auteur comme l'utilisateur connecté
            post.community = community  # Associer le post à la communauté
            post.save()
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

# Vue pour afficher les notifications de l'utilisateur
@login_required
def notification_list(request):
    notifications = Notification.objects.filter(user=request.user, is_read=False)
    return render(request, 'notification_list.html', {'notifications': notifications})

# Vue pour marquer une notification comme lue
@login_required
def mark_notification_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    messages.success(request, "La notification a été marquée comme lue.")
    return redirect('notification_list')

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
