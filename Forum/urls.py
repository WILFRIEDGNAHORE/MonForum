from django.urls import path
from .views.auth_views import register, login_view, user_logout
from .views.community_views import community_list, post_list
from .views.post_views import all_post_list, create_post,  post_detail, vote_down, vote_up
from .views.comment_views import add_comment,   reply_comment, vote, vote_down_comment, vote_up_comment
from .views.post_edit_and_delete_views import edit_post, delete_post
from .views.comment_edit_delete_views import edit_comment, delete_comment
urlpatterns = [
    # Page d'accueil qui redirige vers la vue 'community_list'
    path('', community_list, name='home'),  # Définit 'community_list' comme la page d'accueil
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', user_logout, name='logout'),
    path('communities/', community_list, name='community_list'),
    path('community/<int:community_id>/', post_list, name='post_list'),
    path('community/<int:community_id>/create/', create_post, name='create_post'),
    path('post/<int:post_id>/', post_detail, name='post_detail'),
    path('post/<int:post_id>/comment/', add_comment, name='add_comment'),
    path('comment/<int:comment_id>/edit/', edit_comment, name='edit_comment'),
    path('post/<int:post_id>/vote_up/', vote_up, name='vote_up'),
    path('post/<int:post_id>/vote_down/', vote_down, name='vote_down'),
      path('comment/<int:comment_id>/vote_up/', vote_up_comment, name='vote_up_comment'),
    path('comment/<int:comment_id>/vote_down/', vote_down_comment, name='vote_down_comment'),
    path('comment/<int:comment_id>/reply/', reply_comment, name='reply_comment'),  # Voter pour un commentaire
    path('comment/<int:comment_id>/vote/<str:vote_type>/', vote, {'model': 'comment'}, name='comment_vote'),
    path('all-posts/', all_post_list, name='all_post_list'),
    path('post/<int:post_id>/edit/', edit_post, name='edit_post'),
    path('post/<int:post_id>/delete/', delete_post, name='delete_post'),

    path('comment/<int:comment_id>/delete/',delete_comment, name='delete_comment'),
]
