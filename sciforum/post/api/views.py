from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework import viewsets, permissions, status, pagination
from post.models import Post, Visitors
from user_profile.models import ProfileViewerInfo, Profile
from .serializers import PostSerializer, UserSerializer, CustomUserSerializer,\
    JWTSerializer, VisitorSerializer, ProfileViewerInfoSerializer, PostUpdateSerializer, PostCreateSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
#from django.contrib.auth.mixins import LoginRequiredMixin
from rest_auth.views import LoginView
from rest_auth.registration.views import RegisterView
from rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth.models import User
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from user_profile.models import Profile
from rest_framework_jwt.views import ObtainJSONWebToken
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt import authentication
from .utils import get_client_ip
from django.db.models import Count, Sum
from .mixins import GetSerializerClassMixin

class VisitorsListView(ListAPIView):
    queryset = Visitors.objects.all()
    serializer_class = VisitorSerializer

class ProfileViewerInfoView(ListAPIView):
    queryset = ProfileViewerInfo.objects.all()
    serializer_class = ProfileViewerInfoSerializer

class PostsPagination(pagination.PageNumberPagination):
    page_size = 8

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = PostsPagination
    http_method_names = ['get']

    def retrieve(self, request, *args, **kwargs):
        #viewCounter = Visitors.objects.values('post_id').annotate(viewCount=Count('visitorIp', distinct=True))
        postId = self.get_object().id
        postOwner = self.get_object().owner
        viewCount = 0
        totalPostViewCount = 0

        try:
            viewCount = Visitors.objects.filter(post_id=postId).values('post_id').annotate(viewCount=Count('visitorIp', distinct=True))[0]['viewCount']
        except Exception as exep:
            print(exep)

        newVisitor = Visitors(post=self.get_object(), visitorIp=get_client_ip(request), visitDate=now())
        newVisitor.save()

        try:
            totalPostViewCount = Post.objects.filter(owner=postOwner).aggregate(totalPostViewCount=Sum('viewCount'))['totalPostViewCount']
        except Exception as exep:
            print(exep)

        print(totalPostViewCount)
        profileObj = Profile.objects.get(user=postOwner)
        profileObj.postViews = totalPostViewCount
        profileObj.save(update_fields=('postViews', ))

        obj = self.get_object()
        obj.viewCount = viewCount
        obj.save(update_fields=('viewCount', ))
        return super().retrieve(request, *args, **kwargs)

class PostCreateview(CreateAPIView):
    authentication_classes = [authentication.JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer

class PostUpdateView(UpdateAPIView):
    authentication_classes = [authentication.JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostUpdateSerializer

class UserViewSet(GetSerializerClassMixin, viewsets.ModelViewSet):

    '''here it describes the way of getting user information over the drf depending on the serializer.'''

    queryset = User.objects.all()
    serializer_class = UserSerializer
    serializer_action_classes = {
        'list': CustomUserSerializer,
    }


class UserListView(ListAPIView):
    #permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer

    @action(methods=['get'], detail=True, url_path='retrieve_by_username/(?P<username>\w+)')
    def retrieve_by_username(self, request, username):
        user = get_object_or_404(User, username=username)
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)


class UserDetailView(RetrieveAPIView):
    #authentication_classes = [authentication.JSONWebTokenAuthentication]
    #permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    #serializer_class = UserSerializer
    lookup_field = 'username'

    def get_serializer_class(self):
        #print(self.request.session.get('_auth_user_id', 0))
        #print(self.kwargs['username'])
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

        #print(profileViewCount)

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

        #print(totalPostViewCount)
        profileObj = Profile.objects.get(user=self.get_object())
        profileObj.postViews = totalPostViewCount
        profileObj.save(update_fields=('postViews', ))

        newProfileViewer = ProfileViewerInfo(user=self.get_object(), viewerUsername=requestUser, visitDate=now(), viwer_ip=get_client_ip(request), viwer_agent_info=agent_info)
        newProfileViewer.save()

        return super().retrieve(request, *args, **kwargs)


    '''@action(methods=['get'], detail=True, url_path='retrieve_by_username/(?P<username>\w+)')
    def retrieve_by_username(self, request, username):
        user = get_object_or_404(User, username=username)
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)'''


class UserUpdateView(UpdateAPIView):
    authentication_classes = [authentication.JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'

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
    #serializer_class = JWTSerializer

    def create(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        #token, created = Token.objects.get_or_create(user=user)

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        jwttoken = jwt_encode_handler(payload)

        return Response({
            'token': jwttoken,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
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

