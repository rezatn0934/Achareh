from rest_framework import serializers
from accounts.models import CustomUser


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'last_name', 'password')

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        validated_data['is_active'] = True
        if not password:
            raise serializers.ValidationError('Password is required')
        instance.set_password(password)
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance
