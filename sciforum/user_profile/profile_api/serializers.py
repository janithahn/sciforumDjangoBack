from rest_framework import serializers
from user_profile.models import Profile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user', 'aboutMe', 'creationDate', 'lastAccessDate', 'profileImgUrl', 'views', 'upVotes', 'downVotes', 'facebook', 'linkedIn', 'github']