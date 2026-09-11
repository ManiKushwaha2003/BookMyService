from rest_framework import serializers

from .models import User, ProviderProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def validate_password(self, password):
        if password and len(password)<8:
            raise serializers.ValidationError("Password length must be >= 8")
        return password

    def create(self, validated_data):
        user = super().create(validated_data)

        if user.role=="provider":
            # Create a provider profile on creation
            ProviderProfile.objects.create(user=user)
        return user

    

class ProviderProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProviderProfile
        fields = "__all__"