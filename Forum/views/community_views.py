from django.shortcuts import render, get_object_or_404
from ..models import Community, Post
from django.core.paginator import Paginator

# Vue pour la liste des communautés
def community_list(request):
    communities = Community.objects.all()
    return render(request, 'community_list.html', {'communities': communities})

# Vue pour afficher les posts d'une communauté
def post_list(request, community_id):
    community = get_object_or_404(Community, id=community_id)
    posts = Post.objects.filter(community=community).order_by('-created_at')
    
    # Pagination
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'post_list.html', {'community': community, 'page_obj': page_obj})
