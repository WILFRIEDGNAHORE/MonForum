from django.contrib import admin
from .models import Community, Post, Comment

# Enregistrer le modèle Community
@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at',)
    ordering = ('-created_at',)

# Enregistrer le modèle Post
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'community', 'created_at', 'upvotes', 'downvotes')
    search_fields = ('title', 'content', 'author__username')
    list_filter = ('community', 'created_at')
    ordering = ('-created_at',)

# Enregistrer le modèle Comment
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'content', 'created_at')
    search_fields = ('content', 'user__username')
    list_filter = ('created_at',)
    ordering = ('-created_at',)

