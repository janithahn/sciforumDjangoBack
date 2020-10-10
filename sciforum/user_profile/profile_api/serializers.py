from rest_framework import serializers

from user_profile.models import Profile, UserContact
#from django.contrib.auth.models import User
#from user_profile.profile_api.serializers import UserProfileSerializer

class UserContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserContact
        fields = ['github', 'linkedIn', 'facebook']

class ProfileSerializer(serializers.ModelSerializer):

    #userContact = UserContactSerializer('userContact')

    class Meta:
        model = Profile
        fields = ['user', 'aboutMe', 'profileImg', 'location']
            #, 'lastAccessDate', 'creationDate', 'location', 'views', 'upVotes', 'downVotes', 'profileImgUrl']

    ''' update(self, instance, validated_data):
        # First, update the User
        user_data = validated_data.pop('user', None)
        for attr, value in user_data.items():
            setattr(instance.user, attr, value)
        # Then, update UserProfile
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
        instance.user = validated_data.pop('user', instance.user)
        instance.aboutMe = validated_data.pop('aboutMe', instance.aboutMe)
        instance.lastAccessDate = validated_data.pop('lastAccessDate', instance.lastAccessDate)
        instance.save()
        return instance'''