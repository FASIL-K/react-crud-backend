from rest_framework.serializers import ModelSerializer
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.hashers import make_password


class UserSerializer(ModelSerializer):
    class Meta:
        model=User
        fields = ['id','username','email','password','profile_image']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model.objects.create(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
        
        # def create(self, validated_data):
        #     password = validated_data.pop('password', None)
        #     instance = User.objects.create(**validated_data)
        #     if password is not None:
        #         hashed_password = make_password(password)
        #         print(hashed_password,'daxooooo')
        #         instance.set_password(hashed_password)
        #     instance.save()
        #     return instance


    def update(self, instance, validated_data):
        password = validated_data.get('password')
        if password:
            hashed_password = make_password(password)
            validated_data['password'] = hashed_password
        return super().update(instance, validated_data)
        

class myTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        token['is_admin'] = user.is_superuser

        return token
    