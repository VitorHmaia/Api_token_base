from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from django.http import HttpResponse
from .models import User
import jwt, datetime

# Define uma view para registro de usuários.
class RegisterView(APIView):
    def post(self, request):
        # Cria um serializador com os dados fornecidos na requisição.
        serializer = UserSerializer(data=request.data)
        
        # Valida o serializador, lançando uma exceção se os dados forem inválidos.
        serializer.is_valid(raise_exception=True)
        
        # Salva o usuário no banco de dados usando o serializador.
        serializer.save()
        
        # Retorna os dados do usuário recém-registrado.
        return Response(serializer.data)

# Define uma view para autenticação de usuários.
class LoginView(APIView):
    def post(self, request):
        # Obtém o e-mail e a senha da requisição.
        email = request.data['email']
        password = request.data['password']

        # Filtra o usuário pelo e-mail fornecido.
        user = User.objects.filter(email=email).first()

        # Verifica se o usuário existe.
        if user is None:
            raise AuthenticationFailed('User not found')
        
        # Verifica se a senha fornecida é correta.
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')
        
        # Cria um payload para o token JWT.
        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow() 
        }

        # Gera o token JWT com o payload e uma chave secreta.
        token = jwt.encode(payload, 'secret', algorithm='HS256')

        # Cria uma resposta e configura o cookie com o token JWT.
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }

        return response

# Define uma view para visualização de detalhes do usuário autenticado.
class UserView(APIView):
    def get(self, request):
        # Obtém o token JWT do cookie na requisição.
        token = request.COOKIES.get('jwt')

        # Verifica se o token existe.
        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        
        try:
            # Decodifica o token JWT para obter o payload.
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        
        # Filtra o usuário com base no ID do payload.
        user = User.objects.filter(id=payload['id']).first()
        
        # Cria um serializador para o usuário autenticado e retorna seus dados.
        serializer = UserSerializer(user)
        return Response(serializer.data)

# Define uma view para realizar o logout do usuário.
class LogoutView(APIView):
    def post(self, request):
        # Cria uma resposta.
        response = Response()
        
        # Remove o cookie com o token JWT.
        response.delete_cookie('jwt')
        
        # Define a mensagem de sucesso na resposta.
        response.data = {
            'message': 'success'
        }
        return response
