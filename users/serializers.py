from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


# Create your serializers here.
class RegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = get_user_model()
        fields = ['email', 'username', 'password1', 'password2']

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        password = validated_data.pop('password2')
        user = get_user_model().objects.create_user(username=validated_data['username'], email=validated_data['email'])
        user.set_password(password)
        user.save()
        return user
    

class LoginSerializer(serializers.Serializer):
    identifier = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        identifier = data.get('identifier')
        password = data.get('password')

        if '@' in identifier:
            user = authenticate(request=self.context.get('request'), email=identifier, password=password)
        else:
            user = authenticate(request=self.context.get('request'), username=identifier, password=password)

        if not user:
            raise serializers.ValidationError('Invalid email or password.')

        if not user.is_active:
            raise serializers.ValidationError('User account is disabled.')

        self.user = user
        return data

    def get_user(self):
        return self.user

    def get_tokens(self):
        if hasattr(self, 'user'):
            refresh = RefreshToken.for_user(self.user)
            return {'access_token': str(refresh.access_token), 'refresh_token': str(refresh)}
        raise serializers.ValidationError("User is not authenticated.")
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions', 'date_joined', 'last_login']


