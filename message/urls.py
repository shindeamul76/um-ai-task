from django.urls import path
from .views import MessageView

urlpatterns = [
    path('', MessageView.as_view(), name="message-handler"),
    path('<int:user_id>/', MessageView.as_view(), name="message-history"),
]