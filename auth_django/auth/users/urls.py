from .views import RegisterView, LoginView, UserView, LogoutView
from django.urls import path

urlpatterns = [
    # Define a rota '/register' que usa a classe RegisterView como uma visualização.
    # Essa rota permite que os usuários se registrem.
    path('register', RegisterView.as_view()),
    
    # Define a rota '/login' que usa a classe LoginView como uma visualização.
    # Essa rota permite que os usuários façam login.
    path('login', LoginView.as_view()),
    
    # Define a rota '/user' que usa a classe UserView como uma visualização.
    # Essa rota permite que os usuários vejam informações do próprio perfil.
    path('user', UserView.as_view()),
    
    # Define a rota '/logout' que usa a classe LogoutView como uma visualização.
    # Essa rota permite que os usuários façam logout.
    path('logout', LogoutView.as_view())
]
