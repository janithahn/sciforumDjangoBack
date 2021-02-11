"""sciforum URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from post.api.views import VisitorsListView, ProfileViewerInfoView, PostUpdateView, PostCreateview, PostDeleteView
from user_profile.profile_api.views import CustomAuthToken, CustomLoginView, CustomRegisterView, UserListView, UserDetailView\
    , UserUpdateView, UserDeleteView, JWTLoginView, JWTRegisterView, GoogleLoginView, NewEmailConfirmation, VerifyEmailCustomView
from answer.answer_api.views import AnswerCreateView, AnswerUpdateView, AnswerDeleteView
from vote.vote_api.views import PostVoteCreateview, PostVoteUpdateView, PostVoteDeleteView\
    , AnswerVoteCreateview, AnswerVoteUpdateView, AnswerVoteDeleteView, PostCommentVoteCreateview, PostCommentVoteDeleteView\
    , PostCommentVoteUpdateView , AnswerCommentVoteCreateview, AnswerCommentVoteUpdateView, AnswerCommentVoteDeleteView
# from notification.views import NotificationViewSet
# from user_profile.profile_api.views import ProfileUpdateView, ProfileDetailView
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
# from rest_framework.routers import DefaultRouter
from taggit_suggest.tag_api.views import TagListView
from dj_rest_auth.registration.views import ConfirmEmailView

urlpatterns = [

    path('admin/', admin.site.urls),

    path('api-auth/', include('rest_framework.urls')),

    # basic end-ponits
    path('api/', include('post.api.urls')),
    path('profile_api/', include('user_profile.profile_api.urls')),
    path('answer_api/', include(('answer.answer_api.urls', 'answer'), namespace='answer_api')),
    path('vote_api/', include('vote.vote_api.urls')),

    # post changes
    path('api/post/<int:pk>/update/', PostUpdateView.as_view()),
    path('api/post/create/', PostCreateview.as_view()),
    path('api/post/<int:pk>/delete/', PostDeleteView.as_view()),

    # answer changes
    path('answer_api/answer/<int:pk>/update/', AnswerUpdateView.as_view()),
    path('answer_api/answer/create/', AnswerCreateView.as_view()),
    path('answer_api/answer/<int:pk>/delete/', AnswerDeleteView.as_view()),
    # path("answer_api/answer/notifications/<int:pk>/update", NotificationsUpdateView.as_view()),

    # comments
    path('comment_api/', include('comment.comment_api.urls')),

    # post vote changes
    path('vote_api/postvote/vote/post=<int:post>&owner=<int:owner>/update/', PostVoteUpdateView.as_view()),
    path('vote_api/postvote/vote/create/', PostVoteCreateview.as_view()),
    path('vote_api/postvote/vote/post=<int:post>&owner=<int:owner>/delete/', PostVoteDeleteView.as_view()),

    # post comment vote changes
    path('vote_api/postcommentvote/vote/comment=<int:comment>&owner=<int:owner>/update/', PostCommentVoteUpdateView.as_view()),
    path('vote_api/postcommentvote/vote/create/', PostCommentVoteCreateview.as_view()),
    path('vote_api/postcommentvote/vote/comment=<int:comment>&owner=<int:owner>/delete/', PostCommentVoteDeleteView.as_view()),

    # answer vote changes
    # path('vote_api/answervote/vote/<int:pk>/update/', AnswerVoteUpdateView.as_view()),
    path('vote_api/answervote/vote/answer=<int:answer>&owner=<int:owner>/update/', AnswerVoteUpdateView.as_view()),
    path('vote_api/answervote/vote/create/', AnswerVoteCreateview.as_view()),
    # path('vote_api/answervote/vote/<int:pk>/delete/', AnswerVoteDeleteView.as_view()),
    path('vote_api/answervote/vote/answer=<int:answer>&voteType=<str:voteType>&owner=<int:owner>/delete/', AnswerVoteDeleteView.as_view()),

    # answer comment vote changes
    path('vote_api/answercommentvote/vote/comment=<int:comment>&owner=<int:owner>/update/', AnswerCommentVoteUpdateView.as_view()),
    path('vote_api/answercommentvote/vote/create/', AnswerCommentVoteCreateview.as_view()),
    path('vote_api/answercommentvote/vote/comment=<int:comment>&voteType=<str:voteType>&owner=<int:owner>/delete/', AnswerCommentVoteDeleteView.as_view()),

    path('rest-auth/', include('dj_rest_auth.urls')),

    # for google token
    path('rest-auth/google/', GoogleLoginView.as_view(), name='google_login'),

    path('accounts/', include('allauth.urls')),

    # path('rest-auth/registration/account-confirm-email/<str:key>/', ConfirmEmailView.as_view()), # confirming the email
    path('rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('api-token-auth/', CustomAuthToken.as_view()),

    url(r'^user/login/', CustomLoginView.as_view()),
    url(r'^user/register/', CustomRegisterView.as_view()),

    path('users/', UserListView.as_view()),
    path('users/<str:username>/', UserDetailView.as_view()),
    path('users/<str:username>/update/', UserUpdateView.as_view()),
    path('users/<str:username>/delete/', UserDeleteView.as_view()),
    url(r'^api-jwt-token-auth/', obtain_jwt_token),
    url(r'^api-jwt-token-refresh/', refresh_jwt_token),

    path('jwtlogin/', JWTLoginView.as_view()),
    path('jwtregister/', JWTRegisterView.as_view()),
    url(r'^users/profile/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('rest-auth/account-confirm-email/', VerifyEmailCustomView.as_view(), name='account_email_verification_sent'),
    path('users/profile/account-confirm-email/', NewEmailConfirmation.as_view(), name='account_email_verification_sent'),

    path('postvisitors/', VisitorsListView.as_view()),
    path('profilevisitor/', ProfileViewerInfoView.as_view()),
    path('socialauth/', include('rest_framework_social_oauth2.urls')),
    # path('profile/<int:pk>/', ProfileDetailView.as_view()),
    # path('profile/<int:pk>/update/', ProfileUpdateView.as_view()),

    # notifications
    path('inbox/notifications/', include('notification.urls')),

    # tags
    path('tag_api/tags/', TagListView.as_view()),

    # chat
    path('chat/', include('chat.urls')),

    # news
    path('news/', include('scraper.scraper_api.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

