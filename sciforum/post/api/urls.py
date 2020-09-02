from django.urls import path
from .views import PostDetailView, PostListView

urlpatterns = [
    path('', PostListView.as_view()),
    path('<pk>', PostDetailView.as_view()),
]