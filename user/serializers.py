from rest_framework import serializers

from user.models import User as UserModel

class UserModelSerializer(serializers.ModelSerializer):
    """
        유저 모델 Serializer
    """
    
    class Meta:
        model = UserModel
        fields = "__all__"

    def create(self, validated_data):
        user = UserModel(**validated_data)
        p = user.password
        user.set_password(p)
        user.save()
        return user