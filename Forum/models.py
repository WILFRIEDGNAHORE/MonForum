from django.db import models
from django.contrib.auth.models import User

# Modèle Community
class Community(models.Model):
    name = models.CharField(max_length=100)  # Nom de la communauté
    description = models.TextField()  # Description de la communauté
    created_at = models.DateTimeField(auto_now_add=True)  # Date de création de la communauté
    updated_at = models.DateTimeField(auto_now=True)  # Date de mise à jour de la communauté

    def __str__(self):
        return self.name

# Modèle Post
class Post(models.Model):
    community = models.ForeignKey(Community, related_name='posts', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    upvotes = models.IntegerField(default=0)  # Nombre de votes positifs
    downvotes = models.IntegerField(default=0)  # Nombre de votes négatifs

    def __str__(self):
        return self.title

    def vote_up(self):
        """Incrémente le nombre de votes positifs"""
        self.upvotes += 1
        self.save()

    def vote_down(self):
        """Incrémente le nombre de votes négatifs"""
        self.downvotes += 1
        self.save()

# Modèle Comment
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

    def __str__(self):
        return f"Commentaire de {self.user.username} sur {self.post.title}"

    def vote_up(self):
        self.upvotes += 1
        self.save()

    def vote_down(self):
        self.downvotes += 1
        self.save()

# Modèle Notification
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Utilisateur auquel la notification appartient
    content = models.CharField(max_length=255)  # Contenu de la notification
    is_read = models.BooleanField(default=False)  # Statut de la notification (lue ou non)
    created_at = models.DateTimeField(auto_now_add=True)  # Date de création de la notification

    def __str__(self):
        return f"Notification pour {self.user.username}: {self.content}"

