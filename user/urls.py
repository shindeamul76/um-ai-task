from django.urls import path
from .views import (
    UserCreateView,
    UserListView,
    UserDetailView,
    FetchQuestionsView,
    SubmitResponsesView,
)

urlpatterns = [
    # User Management APIs
    path('', UserListView.as_view(), name='user-list'),  # GET /users/
    path('create/', UserCreateView.as_view(), name='user-create'),  # POST /users/
    path('<int:user_id>/', UserDetailView.as_view(), name='user-detail'),  # GET, PUT, DELETE /users/<user_id>/

    # Question APIs
    path('<int:user_id>/questions/', FetchQuestionsView.as_view(), name='fetch-questions'),  # GET /users/<user_id>/questions/
    path('<int:user_id>/responses/', SubmitResponsesView.as_view(), name='submit-responses'),  # POST /users/<user_id>/responses/
]