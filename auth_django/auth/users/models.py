from django.db import models
from django.contrib.auth.models import AbstractUser

# Definição da classe User que herda de AbstractUser
class User(AbstractUser):
    # Campo para o nome do usuário
    name = models.CharField(max_length=255)
    # Campo para o email do usuário, único no sistema
    email = models.CharField(max_length=255, unique=True)
    # Campo para a senha do usuário
    password = models.CharField(max_length=255)
    # Não será utilizado o campo username padrão do AbstractUser
    username = None

    # Define que o campo utilizado para fazer login é o email
    USERNAME_FIELD = 'email'
    # Campos obrigatórios ao criar um usuário (neste caso, nenhum)
    REQUIRED_FIELDS = []
