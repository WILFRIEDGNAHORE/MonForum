from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from ..forms import UserRegisterForm

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
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('community_list')
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    return render(request, 'login.html')

# Vue pour la déconnexion
def user_logout(request):
    logout(request)
    messages.info(request, "Vous êtes maintenant déconnecté.")
    return redirect('login')
