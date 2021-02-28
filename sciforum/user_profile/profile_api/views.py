from .serializers import ProfileSerializer
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, CharFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView, CreateAPIView, DestroyAPIView, get_object_or_404
from rest_framework import viewsets, permissions, status #, pagination
from post.models import Post
from user_profile.models import ProfileViewerInfo, Profile, UserEmployment, UserEducation, UserLanguages\
    , UserContact, UserSkills, UserInterests
from .serializers import UserSerializer, CustomUserSerializer, JWTSerializer, UserEmploymentSerializer\
    , UserEducationSerializer, UserLanguageSerializer, UserSkillsSerializer, UserContactSerializer\
    , MentionListSerializer, UserInterestsSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
# from django.contrib.auth.mixins import LoginRequiredMixin
from rest_auth.views import LoginView
from dj_rest_auth.registration.views import RegisterView, SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth.models import User
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from rest_framework_jwt.views import ObtainJSONWebToken
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt import authentication
from .utils import get_client_ip
from django.db.models import Count, Sum
from .mixins import GetSerializerClassMixin
from firebase_admin import auth
from dj_rest_auth.registration.views import VerifyEmailView
from django.utils.translation import ugettext_lazy as _
from django.forms.models import model_to_dict

# email confirmation
from allauth.account.signals import email_confirmed
from django.dispatch import receiver

from allauth.account.utils import send_email_confirmation
from rest_framework.views import APIView
from allauth.account.admin import EmailAddress
from rest_framework.exceptions import APIException
from rest_framework.fields import CurrentUserDefault

from notifications.signals import notify


class ProfileViewSet(viewsets.ModelViewSet):
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'user'
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['aboutMe', 'user']
    http_method_names = ['get']


class ProfileUpdateViewSet(viewsets.ModelViewSet):
    authentication_classes = [authentication.JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'user'
    http_method_names = ['put', 'patch']

    def perform_update(self, serializer):
        # Check if an image exists for the profile object and if yes then delete the image from the storage
        prev_image = self.get_object().profileImg
        if prev_image:
            prev_image.delete()
        serializer.save()


# views for users
class UserViewSet(GetSerializerClassMixin, viewsets.ModelViewSet):
    authentication_classes = [authentication.JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    '''
        here it describes the way of getting user information over the drf depending on the serializer.
    '''

    queryset = User.objects.all()
    serializer_class = UserSerializer
    serializer_action_classes = {
        'list': CustomUserSerializer,
    }


class UserListView(ListAPIView):
    # permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer

    @action(methods=['get'], detail=True, url_path='retrieve_by_username/(?P<username>\w+)')
    def retrieve_by_username(self, request, username):
        user = get_object_or_404(User, username=username)
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)


class UserDetailView(RetrieveAPIView):
    # authentication_classes = [authentication.JSONWebTokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    # serializer_class = UserSerializer
    lookup_field = 'username'

    def get_serializer_class(self):
        # print(self.request.session.get('_auth_user_id', 0))
        # print(self.kwargs['username'])
        user = self.request.user
        if user.is_authenticated and user.username == self.kwargs['username']:
            return UserSerializer
        return CustomUserSerializer

    def retrieve(self, request, *args, **kwargs):
        user = self.get_object()
        profileViewCount = 0
        totalPostViewCount = 0
        agent_info = ''
        requestUser = ''

        try:
            profileViewCount = ProfileViewerInfo.objects.filter(user=user).values('user').annotate(viewCount=Count('viwer_ip', distinct=True))[0]['viewCount']
        except Exception as exep:
            print(exep)

        # print(profileViewCount)

        try:
            agent_info = request.META.get('HTTP_USER_AGENT', '<unknown>')[:255]
        except Exception as exep:
            print(exep)

        try:
            requestUser = request.user
        except Exception as exep:
            print(exep)

        try:
            totalPostViewCount = Post.objects.filter(owner=self.get_object()).aggregate(totalPostViewCount=Sum('viewCount'))['totalPostViewCount']
        except Exception as exep:
            print(exep)

        # print(totalPostViewCount)
        profileObj = Profile.objects.get(user=self.get_object())
        profileObj.postViews = totalPostViewCount
        profileObj.save(update_fields=('postViews', ))

        newProfileViewer = ProfileViewerInfo(user=self.get_object(), viewerUsername=requestUser, visitDate=now(), viwer_ip=get_client_ip(request), viwer_agent_info=agent_info)
        newProfileViewer.save()

        return super().retrieve(request, *args, **kwargs)


    '''
    @action(methods=['get'], detail=True, url_path='retrieve_by_username/(?P<username>\w+)')
    def retrieve_by_username(self, request, username):
        user = get_object_or_404(User, username=username)
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
    '''


class UserUpdateView(UpdateAPIView):
    # authentication_classes = [authentication.JSONWebTokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'

    def perform_update(self, serializer):
        UserInterests.objects.filter(user=self.request.user).delete()  # first delete existing values before update
        serializer.save()


class UserDeleteView(DestroyAPIView):
    authentication_classes = [authentication.JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'


# User Credentials
class UserEmploymentFilter(FilterSet):
    username = CharFilter(field_name='user__username', lookup_expr='iexact')

    class Meta:
        model = UserEmployment
        fields = ('username',)


class UserEmploymentViewSet(viewsets.ModelViewSet):
    queryset = UserEmployment.objects.all()
    serializer_class = UserEmploymentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserEmploymentFilter
    # filterset_fields = ['user__username']
    http_method_names = ['get']

    '''def get_queryset(self):
        """
        filtering against a `username` query parameter in the URL.
        """
        queryset = UserEmployment.objects.all()
        username = self.request.query_params.get('username', None)
        if username is not None:
            queryset = queryset.filter(user__username=username)
        return queryset'''


class UserEmploymentEditViewSet(viewsets.ModelViewSet):

    authentication_classes = [authentication.JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    queryset = UserEmployment.objects.all()
    serializer_class = UserEmploymentSerializer

    http_method_names = ['get', 'post', 'patch', 'put', 'delete']


class UserEducationFilter(FilterSet):
    username = CharFilter(field_name='user__username', lookup_expr='iexact')

    class Meta:
        model = UserEducation
        fields = ('username',)


class UserEducationViewSet(viewsets.ModelViewSet):

    queryset = UserEducation.objects.all()
    serializer_class = UserEducationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserEducationFilter

    http_method_names = ['get']


class UserEducationEditViewSet(viewsets.ModelViewSet):

    authentication_classes = [authentication.JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    queryset = UserEducation.objects.all()
    serializer_class = UserEducationSerializer

    http_method_names = ['get', 'post', 'patch', 'put', 'delete']


class UserLanguagesFilter(FilterSet):
    username = CharFilter(field_name='user__username', lookup_expr='iexact')

    class Meta:
        model = UserLanguages
        fields = ('username',)


class UserLanguagesViewSet(viewsets.ModelViewSet):

    queryset = UserLanguages.objects.all()
    serializer_class = UserLanguageSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_class = UserLanguagesFilter

    http_method_names = ['get']


class UserLanguagesEditViewSet(viewsets.ModelViewSet):

    authentication_classes = [authentication.JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    queryset = UserLanguages.objects.all()
    serializer_class = UserLanguageSerializer

    http_method_names = ['get', 'post', 'patch', 'put', 'delete']


class UserSkillsFilter(FilterSet):
    username = CharFilter(field_name='user__username', lookup_expr='iexact')

    class Meta:
        model = UserSkills
        fields = ('username',)


class UserSkillsViewSet(viewsets.ModelViewSet):
    queryset = UserSkills.objects.all()
    serializer_class = UserSkillsSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_class = UserSkillsFilter

    http_method_names = ['get']


class UserSkillsEditViewSet(viewsets.ModelViewSet):

    authentication_classes = [authentication.JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    queryset = UserSkills.objects.all()
    serializer_class = UserSkillsSerializer

    http_method_names = ['get', 'post', 'patch', 'put', 'delete']


class UserInterestsFilter(FilterSet):
    username = CharFilter(field_name='user__username', lookup_expr='iexact')

    class Meta:
        model = UserInterests
        fields = ('username',)


class UserInterestsViewSet(viewsets.ModelViewSet):
    queryset = UserInterests.objects.all()
    serializer_class = UserInterestsSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_class = UserInterestsFilter

    http_method_names = ['get']


class UserInterestsEditViewSet(viewsets.ModelViewSet):

    authentication_classes = [authentication.JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    queryset = UserInterests.objects.all()
    serializer_class = UserInterestsSerializer

    http_method_names = ['get', 'post', 'patch', 'put', 'delete']


class UserContactFilter(FilterSet):
    username = CharFilter(field_name='user__username', lookup_expr='iexact')

    class Meta:
        model = UserSkills
        fields = ('username',)


class UserContactViewSet(viewsets.ModelViewSet):
    queryset = UserContact.objects.all()
    serializer_class = UserContactSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_class = UserContactFilter

    http_method_names = ['get']


class UserContactEditViewSet(viewsets.ModelViewSet):
    authentication_classes = [authentication.JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    queryset = UserContact.objects.all()
    serializer_class = UserContactSerializer

    http_method_names = ['get', 'post', 'patch', 'put', 'delete']


class MentionListViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = MentionListSerializer
    # http_method_names = ['get']


# views for authentication
class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        '''try:
            request_user, data = request.get_parameters(request)
            user = request.get_user_by_username(data['username'])
            update_last_login(None, user)
        except Exception as exc:
            return None'''

        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username,
            'email': user.email
        })


# JWT Views
class JWTLoginView(ObtainJSONWebToken):
    serializer_class = JWTSerializer


class JWTRegisterView(RegisterView):
    # serializer_class = JWTSerializer

    def create(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        # token, created = Token.objects.get_or_create(user=user)

        Profile.objects.update_or_create(user=user)  # creating user profile when the user is registered

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        jwttoken = jwt_encode_handler(payload)

        firebase_token = auth.create_custom_token(user.username)

        # user notification about account verification
        from_user = User.objects.get(username='admin')
        to_user = user
        message = 'Account verification link has been sent to your email. Please verify your account.'
        notify.send(sender=from_user, recipient=to_user, verb=message, description='email_verification')

        return Response({
            'token': jwttoken,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'email_verified': False,
                'has_interests': False,
                'is_email_subscribed': False,
            },
            'firebase_token': firebase_token
        })


class GoogleLoginView(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter

    def get_response(self):
        # get_adapter(self.request).login(self.request, self.user)

        Profile.objects.update_or_create(user=self.user)

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        user = self.user

        firebase_token = auth.create_custom_token(user.username)

        payload = jwt_payload_handler(user)
        jwttoken = jwt_encode_handler(payload)

        email_verified = EmailAddress.objects.get(user=user).verified

        user_profile = Profile.objects.get(user=user)
        user_role = user_profile.userRole.value
        is_email_subscribed = user_profile.is_email_subscribed

        has_interests = False
        if UserInterests.objects.filter(user=user).count() != 0:
            has_interests = True

        return Response({
            'token': jwttoken,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'email_verified': email_verified,
                'role': user_role,
                'has_interests': has_interests,
                'is_email_subscribed': is_email_subscribed,
            },
            'firebase_token': firebase_token,
        })


class CustomLoginView(LoginView):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        Profile.objects.filter(pk=user).update(lastAccessDate=now())
        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username,
            'email': user.email
        })


class CustomRegisterView(RegisterView):

    def create(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username,
            'email': user.email
        })


# Account confirmation email
@receiver(email_confirmed)
def email_confirmed_(request, email_address, **kwargs):
    user = email_address.user
    user.email_verified = True

    user.save()


class EmailConfirmation(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if request.user.email_verified:
            return Response({'message': 'Email already verified'}, status=status.HTTP_201_CREATED)

        send_email_confirmation(request, request.user)
        return Response({'message': 'Email confirmation sent'}, status=status.HTTP_201_CREATED)


class NewEmailConfirmation(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = get_object_or_404(User, email=request.data['email'])
        emailAddress = EmailAddress.objects.filter(user=user, verified=True).exists()

        if emailAddress:
            return Response({'message': 'This email is already verified'}, status=status.HTTP_200_OK)
        else:
            try:
                send_email_confirmation(request, user=user)
                return Response({'message': 'Email confirmation sent'}, status=status.HTTP_201_CREATED)
            except APIException:
                return Response({'message': 'This email does not exist, please create a new account'}, status=status.HTTP_403_FORBIDDEN)


class VerifyEmailCustomView(VerifyEmailView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = self.request.user
        try:
            emailAddress = EmailAddress.objects.filter(user=user, verified=True).exists()
            if emailAddress:
                return Response({'detail': 'already_verified'}, status=status.HTTP_200_OK)
        except Exception as exp:
            print(exp)

        # deleting notification if exists
        from_user = User.objects.get(username='admin')
        to_user = user
        try:
            notification = to_user.notifications.filter(actor_object_id=from_user.id, recipient=user,
                                                        description='email_verification')
            notification.delete()
        except Exception as exp:
            print(exp)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.kwargs['key'] = serializer.validated_data['key']
        confirmation = self.get_object()
        confirmation.confirm(self.request)
        return Response({'detail': _('ok')}, status=status.HTTP_200_OK)


