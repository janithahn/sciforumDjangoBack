from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, user_logged_in
from rest_framework_jwt.serializers import JSONWebTokenSerializer, jwt_payload_handler, jwt_encode_handler
from enumfields.drf.serializers import EnumSupportSerializerMixin
from user_profile.models import Profile, UserContact, UserLanguages, UserEducation, UserEmployment, UserSkills
from answer.models import Answer
from post.models import Post
# from django.contrib.auth.models import User
# from user_profile.profile_api.serializers import UserProfileSerializer
# from drf_writable_nested.serializers import WritableNestedModelSerializer


class UserContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserContact
        fields = ['github', 'linkedIn', 'facebook']


class UserLanguageSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserLanguages
        fields = ['id', 'user', 'language']


class UserEducationSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserEducation
        fields = ['id', 'user', 'school', 'degree', 'field_of_study', 'start_year', 'end_year', 'description']


class UserEmploymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserEmployment
        fields = ['id', 'user', 'position', 'company', 'start_year', 'end_year', 'currently_work']


class UserSkillsSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserSkills
        fields = ['id', 'user', 'skill']


class ProfileSerializer(serializers.ModelSerializer):

    # userContact = UserContactSerializer('userContact')
    # picture_url = serializers.SerializerMethodField('get_picture_url')
    profileImg = serializers.ImageField(use_url=True)

    class Meta:
        model = Profile
        fields = ['user', 'aboutMe', 'profileImg', 'location']
            # , 'lastAccessDate', 'creationDate', 'location', 'views', 'upVotes', 'downVotes', 'profileImgUrl']

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
            'login_ip': {'write_only': True},
            'user_agent_info': {'write_only': True},
            'postViews': {'read_only': True},
        }

    '''def create(self, validated_data):
        user_contact_data = validated_data.pop('userContact')
        profile = Profile.objects.create(**validated_data)
        for contact in user_contact_data:
            UserContact.objects.create(profile=profile, **contact)
        return profile

    def update(self, instance, validated_data):
        user_contact_data = validated_data.pop('userContact', None)
        print(user_contact_data)
        # UserContact.objects.update_or_create(profile=instance, defaults=user_contact_data)
        return super(CustomProfileSerializer, self).update(instance, validated_data)'''


class CustomUserSerializer(serializers.ModelSerializer):
    profile = CustomProfileSerializer('profile', partial=True)
    contact = UserContactSerializer('contact', read_only=True)
    employment = UserEmploymentSerializer('employment', partial=True, many=True, read_only=True)
    education = UserEducationSerializer('education', partial=True, many=True, read_only=True)
    languages = UserLanguageSerializer('languages', partial=True, many=True, read_only=True)
    skills = UserSkillsSerializer('skills', partial=True, many=True, read_only=True)
    answers = serializers.SerializerMethodField(read_only=True)
    posts = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'profile', 'contact', 'employment', 'education', 'languages', 'skills', 'answers', 'posts']

    def get_answers(self, obj):
        return Answer.objects.filter(owner=obj.id).count()

    def get_posts(self, obj):
        return Post.objects.filter(owner=obj.id).count()


class UserSerializer(serializers.ModelSerializer):  # you can try WritableNestedModelSerializer here
    profile = CustomProfileSerializer('profile', partial=True)
    contact = UserContactSerializer('contact', partial=True)
    employment = UserEmploymentSerializer('employment', partial=True, many=True)
    education = UserEducationSerializer('education', partial=True, many=True)
    languages = UserLanguageSerializer('languages', partial=True, many=True)
    skills = UserSkillsSerializer('skills', partial=True, many=True)
    last_login = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    answers = serializers.SerializerMethodField(read_only=True)
    posts = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'last_login', 'profile', 'contact', 'employment', 'education', 'languages', 'skills', 'answers', 'posts']

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

    def get_answers(self, obj):
        return Answer.objects.filter(owner=obj.id).count()

    def get_posts(self, obj):
        return Post.objects.filter(owner=obj.id).count()

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', None)
        user_contact_data = validated_data.pop('contact', None)
        user_employment_data = validated_data.pop('employment', None)
        user_education_data = validated_data.pop('education', None)
        user_languages_data = validated_data.pop('languages', None)
        user_skills_data = validated_data.pop('skills', None)
        user = super(UserSerializer, self).create(validated_data)
        self.update_or_create_profile(user, profile_data, user_contact_data, user_employment_data, user_education_data, user_languages_data, user_skills_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        user_contact_data = validated_data.pop('contact', None)
        user_employment_data = validated_data.pop('employment', None)
        user_education_data = validated_data.pop('education', None)
        user_languages_data = validated_data.pop('languages', None)
        user_skills_data = validated_data.pop('skills', None)
        self.update_or_create_profile(instance, profile_data, user_contact_data, user_employment_data, user_education_data, user_languages_data, user_skills_data)
        return super(UserSerializer, self).update(instance, validated_data)

    def update_or_create_profile(self, user, profile_data, user_contact_data, user_employment_data, user_education_data, user_languages_data, user_skills_data):
        # This always creates a Profile if the User is missing one
        # change the logic here if that's not right for your app

        Profile.objects.update_or_create(user=user, defaults=profile_data)
        UserContact.objects.update_or_create(user=user, defaults=user_contact_data)

        if user_employment_data:
            for employment in user_employment_data:
                UserContact.objects.update_or_create(user=user, **employment)

        if user_education_data:
            for education in user_education_data:
                UserEducation.objects.update_or_create(user=user, **education)

        if user_languages_data:
            for language in user_languages_data:
                UserLanguages.objects.update_or_create(user=user, **language)

        if user_skills_data:
            for skill in user_skills_data:
                UserSkills.objects.update_or_create(user=user, **skill)


class UserprofileImgSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ['profileImg']


class MentionListSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'avatar']

    def get_avatar(self, obj):
        request = self.context.get('request')
        try:
            avatar_url = Profile.objects.get(user=obj).profileImg.url
            return request.build_absolute_uri(avatar_url)
        except Exception as exp:
            print(exp)
        return None


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