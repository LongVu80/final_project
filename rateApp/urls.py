from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('login/', views.login),
    path('register/', views.register),
    path('success/', views.success),
    path('view-officials', views.view_officials),
    path('show-officials', views.show_officials),
    path('rate/<str:name>/<str:elected_office>', views.rate_official),
    path('logout', views.logout),
    path('message', views.message),
    path('comment', views.comment),
    path('deleteMessage/<int:message_id>', views.deleteMessage),
    path('deleteComment/<int:comment_id>', views.deleteComment),
]