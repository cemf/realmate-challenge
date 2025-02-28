from django.urls import path
from .views import ConversationDetailView

urlpatterns = [
    path('conversations/<uuid:id>', ConversationDetailView.as_view(), name='conversation-detail'),
]