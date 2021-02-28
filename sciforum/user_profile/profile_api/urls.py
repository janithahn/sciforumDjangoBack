from django.urls import path
# from .views import PostDetailView, PostListView, PostCreateView, PostUpdateView, PostDeleteView
from user_profile.profile_api.views import ProfileViewSet, UserViewSet, UserEmploymentViewSet, UserEmploymentEditViewSet\
    , UserEducationViewSet, UserEducationEditViewSet, UserLanguagesViewSet, UserLanguagesEditViewSet, UserSkillsViewSet\
    , UserSkillsEditViewSet, UserContactViewSet, UserContactEditViewSet, MentionListViewSet, UserInterestsViewSet\
    , UserInterestsEditViewSet, ProfileUpdateViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'', ProfileViewSet, basename='profile_api')
router.register(r'users/update_view', ProfileUpdateViewSet, basename='profile_update_view')
router.register(r'users/viewset', UserViewSet, basename='users')

router.register(r'user_employment/viewset', UserEmploymentViewSet, 'user_employment')
router.register(r'user_employment_edit/viewset', UserEmploymentEditViewSet, 'user_employment')

router.register(r'user_education/viewset', UserEducationViewSet, 'user_education')
router.register(r'user_education_edit/viewset', UserEducationEditViewSet, 'user_education')

router.register(r'user_skills/viewset', UserSkillsViewSet, 'user_skills')
router.register(r'user_skills_edit/viewset', UserSkillsEditViewSet, 'user_skills')

router.register(r'user_interests/viewset', UserInterestsViewSet, 'user_interests')
router.register(r'user_interests_edit/viewset', UserInterestsEditViewSet, 'user_interests')

router.register(r'user_languages/viewset', UserLanguagesViewSet, 'user_languages')
router.register(r'user_languages_edit/viewset', UserLanguagesEditViewSet, 'user_languages')

router.register(r'user_contact/viewset', UserContactViewSet, 'user_contact')
router.register(r'user_contact_edit/viewset', UserContactEditViewSet, 'user_contact')

router.register(r'mentions/list', MentionListViewSet, 'mentions')

urlpatterns = router.urls
