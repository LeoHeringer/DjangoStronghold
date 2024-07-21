from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'creation_date']
        extra_kwargs = {
            'name': {'help_text': 'Nome completo do usuário'},
            'email': {'help_text': 'Endereço de email do usuário'},
        }
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value
