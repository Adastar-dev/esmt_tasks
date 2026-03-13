from django.urls import path
from . import views

urlpatterns = [
    path('projets/<int:projet_id>/messages/', views.MessageListView.as_view(), name='messages'),
    path('projets/<int:projet_id>/chat/', views.chat_projet, name='chat_projet'),
]