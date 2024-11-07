from django.urls import path
from . import views

urlpatterns = [
    # Routes pour l'authentification
    path('register/', views.register, name='register'),  # Page d'inscription
    path('login/', views.login_view, name='login'),  # Page de connexion
    path('logout/', views.user_logout, name='logout'),  # Déconnexion

    # Routes pour les communautés et les posts
    path('', views.community_list, name='community_list'),  # Liste des communautés
    path('community/<int:community_id>/', views.post_list, name='post_list'),  # Liste des posts dans une communauté spécifique
    path('community/<int:community_id>/create/', views.create_post, name='create_post'),  # Créer un post dans une communauté
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),  # Détails d'un post

    # Route pour les commentaires et les votes
    path('post/<int:post_id>/vote/<str:vote_type>/', views.vote, {'model': 'post'}, name='post_vote'),
      path('post/<int:post_id>/add_comment/', views.add_comment, name='add_comment'),  # Voter pour un post
    path('comment/<int:comment_id>/vote/<str:vote_type>/', views.vote, {'model': 'comment'}, name='comment_vote'),
      path('post/<int:post_id>/vote_up/', views.vote_up, name='vote_up'),
    path('post/<int:post_id>/vote_down/', views.vote_down, name='vote_down'),
      path('comment/<int:comment_id>/vote_up/', views.vote_up_comment, name='vote_up_comment'),
    path('comment/<int:comment_id>/vote_down/', views.vote_down_comment, name='vote_down_comment'),
    path('comment/<int:comment_id>/reply/', views.reply_comment, name='reply_comment'),  # Voter pour un commentaire

    # Routes pour les notifications
    path('notifications/', views.notification_list, name='notification_list'),  # Liste des notifications
    path('notification/<int:notification_id>/mark-read/', views.mark_notification_read, name='mark_notification_read'),  # Marquer une notification comme lue
]
