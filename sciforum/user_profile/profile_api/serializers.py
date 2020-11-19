from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, user_logged_in
from rest_framework_jwt.serializers import JSONWebTokenSerializer, jwt_payload_handler, jwt_encode_handler
from enumfields.drf.serializers import EnumSupportSerializerMixin
from user_profile.models import Profile, UserContact
# from django.contrib.auth.models import User
# from user_profile.profile_api.serializers import UserProfileSerializer
# from drf_writable_nested.serializers import WritableNestedModelSerializer

class UserContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserContact
        fields = ['github', 'linkedIn', 'facebook']

class ProfileSerializer(serializers.ModelSerializer):

    # userContact = UserContactSerializer('userContact')
    # picture_url = serializers.SerializerMethodField('get_picture_url')
    profileImg = serializers.ImageField(use_url=True)

    class Meta:
        model = Profile
        fields = ['user', 'aboutMe', 'profileImg', 'location']
            #, 'lastAccessDate', 'creationDate', 'location', 'views', 'upVotes', 'downVotes', 'profileImgUrl']

    def get_picture_url(self, profile):
        print(profile.profileImg.url)
        return profile.profileImg.url

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

class CustomProfileSerializer(EnumSupportSerializerMixin, serializers.ModelSerializer):

    lastAccessDate = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    # login_ip = serializers.IPAddressField(write_only=True)

    class Meta:
        model = Profile
        fields = ['aboutMe', 'profileImg', 'location', 'lastAccessDate', 'postViews', 'login_ip', 'user_agent_info']
            #, 'userRole']
        extra_kwargs = {
            'login_ip': { 'write_only': True },
            'user_agent_info': { 'write_only': True },
            'postViews': { 'read_only': True },
        }

class CustomUserSerializer(serializers.ModelSerializer):
    profile = CustomProfileSerializer('profile')

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'profile']

class UserSerializer(serializers.ModelSerializer): # you can try WritableNestedModelSerializer here
    profile = CustomProfileSerializer('profile')
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

class UserprofileImgSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ['profileImg']

class JWTUserSerializer(serializers.ModelSerializer):

    profile = UserprofileImgSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile']

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