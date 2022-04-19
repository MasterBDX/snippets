from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()

class AddUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        style={'input_type': 'password',"min_linght":8}
    )

    class Meta:
        model = User
        fields = ['phone_number',"username","email","password"]
        
        extra_kwargs = {'password': {'write_only': True}}
        
        def create(self, validated_data):
            user = User.objects.create_user(**validated_data)
            return user

   

