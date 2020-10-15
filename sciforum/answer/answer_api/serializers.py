from rest_framework import serializers

from answer.models import Answer

class AnswerSerializer(serializers.ModelSerializer):

    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    #owner = serializers.CharField(source='owner.username')

    class Meta:
        model = Answer
        fields = ['id', 'postBelong', 'owner', 'answerContent', 'created_at', 'updated_at']

class AnswerCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = ['postBelong', 'owner', 'answerContent']

class AnswerUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = ['answerContent']