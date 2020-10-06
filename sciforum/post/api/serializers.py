from rest_framework import serializers
from post.models import Post
from django.contrib.auth.models import User
from user_profile.models import Profile, ProfileImage
#from user_profile.profile_api.serializers import ProfileSerializer
#from drf_writable_nested.serializers import WritableNestedModelSerializer

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'owner', 'title', 'body', 'viewCount']

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ['aboutMe', 'profileImg', 'location', 'displayName']
            #, 'lastAccessDate']

class ProfileImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProfileImage
        fields = ['id', 'profileImg']

class CustomUserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer('profile')

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'profile']

class UserSerializer(serializers.ModelSerializer): # you can try WritableNestedModelSerializer here
    profile = ProfileSerializer('profile')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'profile']

        '''def update(self, instance, validated_data):
        #profile_data = validated_data.pop('profile')
        profile = instance.profile
        print(instance)
        #instance.pk = validated_data.get('pk', profile.pk)
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()

        profile.save()

        return instance'''

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', None)
        user = super(UserSerializer, self).create(validated_data)
        self.update_or_create_profile(user, profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        self.update_or_create_profile(instance, profile_data)
        return super(UserSerializer, self).update(instance, validated_data)

    def update_or_create_profile(self, user, profile_data):
        # This always creates a Profile if the User is missing one;
        # change the logic here if that's not right for your app
        Profile.objects.update_or_create(user=user, defaults=profile_data)