from django import forms
from django.contrib.auth.models import User
from .models import Post, Comment, Community, Notification

# Formulaire d'inscription
class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Mot de passe'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirmer le mot de passe'}), label="Confirmer le mot de passe")

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Nom d’utilisateur'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Adresse email'}),
        }

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")
        return password2

# Formulaire de création de post
class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'community']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Titre du post'}),
            'content': forms.Textarea(attrs={'placeholder': 'Contenu du post', 'rows': 5}),
            'community': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['community'].queryset = Community.objects.all()

# Formulaire de commentaire
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': 'Votre commentaire...', 'rows': 4, 'cols': 40}),
        }

# Formulaire de vote
class VoteForm(forms.Form):
    CHOICES = [
        ('upvote', 'Upvote'),
        ('downvote', 'Downvote')
    ]
    vote = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
