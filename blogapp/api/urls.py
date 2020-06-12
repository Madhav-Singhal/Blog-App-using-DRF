from django.urls import path, include

from .views import (
    PostListView, 
    PostDetailView, 
    PostUpdateView, 
    PostDeleteView,
    PostCreateView,
    CommentListView,
    CommentDetailView,
    CommentCreateView
)

app_name='api'

urlpatterns = [
    path('', PostListView.as_view(), name = 'list'),
    # path('api-auth/', include('rest_framework.urls')),
    path('create/', PostCreateView.as_view(), name = 'create'),
    path('<pk>/detail/', PostDetailView.as_view(), name = 'detail'),
    path('<pk>/edit/', PostUpdateView.as_view(), name = 'edit'),
    path('<pk>/delete/', PostDeleteView.as_view(), name = 'delete'),

    path('comments/', CommentListView.as_view(), name = 'c-list'),
    path('comments/<pk>/c-detail/', CommentDetailView.as_view(), name = 'c-detail'),
    path('comments/<pk>/c-create/', CommentCreateView.as_view(), name = 'c-create'),
    path('comments/<pk>/<parent_id>/r-create/', CommentCreateView.as_view(), name = 'r-create'),




]