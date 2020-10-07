from post.models import Post
from django.contrib.auth.models import User
from user_profile.models import Profile
from django.contrib.auth import authenticate, user_logged_in
from rest_framework import serializers
from rest_framework_jwt.serializers import JSONWebTokenSerializer, jwt_payload_handler, jwt_encode_handler
#from user_profile.profile_api.serializers import ProfileSerializer
#from drf_writable_nested.serializers import WritableNestedModelSerializer

class PostSerializer(serializers.ModelSerializer):

    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'owner', 'title', 'body', 'viewCount', 'created_at', 'updated_at']

class ProfileSerializer(serializers.ModelSerializer):

    lastAccessDate = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Profile
        fields = ['aboutMe', 'profileImg', 'location', 'displayName', 'lastAccessDate', 'login_ip', 'user_agent_info']

class CustomUserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer('profile')

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'profile']

class JWTUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class UserSerializer(serializers.ModelSerializer): # you can try WritableNestedModelSerializer here
    profile = ProfileSerializer('profile')
    last_login = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'last_login', 'profile']

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

class JWTSerializer(JSONWebTokenSerializer):
    def validate(self, attrs):
        credentials = {
            self.username_field: attrs.get(self.username_field),
            'password': attrs.get('password')
        }

        if all(credentials.values()):
            user = authenticate(request=self.context['request'], **credentials)

            if user:
                if not user.is_active:
                    msg = 'User account is disabled.'
                    raise serializers.ValidationError(msg)

                payload = jwt_payload_handler(user)
                user_logged_in.send(sender=user.__class__, request=self.context['request'], user=user)
                print(user)
                return {
                    'token': jwt_encode_handler(payload),
                    'user': user
                }
            else:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg)
        else:
            msg = 'Must include "{username_field}" and "password".'
            msg = msg.format(username_field=self.username_field)
            raise serializers.ValidationError(msg)