from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    # Define um serializador para o modelo User.
    class Meta:
        # Define o modelo que será serializado.
        model = User
        
        # Define que todos os campos do modelo serão incluídos no serializador.
        fields = '__all__'
        
        # Define argumentos extras, convertendo a senha apenas para escrita, ou seja, não pode sre visualizada num método GET
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    # Define uma função para criar um novo usuário com os dados validados.
    def create(self, validated_data):
        # Remove a senha dos dados validados para tratá-la separadamente.
        password = validated_data.pop('password', None)
        
        # Cria uma instância do modelo User com os dados validados.
        instance = self.Meta.model(**validated_data)
        
        # Se uma senha foi fornecida, define a senha usando o método set_password.
        if password is not None:
            instance.set_password(password)
        
        # Salva a instância no banco de dados.
        instance.save()
        
        # Retorna a instância recém-criada.
        return instance
