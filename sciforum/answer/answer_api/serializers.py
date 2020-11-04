from rest_framework import serializers
from answer.models import Answer

class AnswerSerializer(serializers.ModelSerializer):

    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    ownerDisplayName = serializers.CharField(source='owner.username')
    ownerAvatar = serializers.ImageField(source='owner.profile.profileImg')

    class Meta:
        model = Answer
        fields = ['id', 'postBelong', 'owner', 'ownerDisplayName', 'ownerAvatar', 'answerContent', 'created_at', 'updated_at']

class AnswerCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = ['postBelong', 'owner', 'answerContent']

class AnswerUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = ['answerContent']
