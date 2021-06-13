from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('login/', views.login),
    path('register/', views.register),
    path('success/', views.success),
    path('daily/', views.daily),
    path('view_officials', views.view_officials),
    path('show_officials/', views.show_officials),
    path('officials/', views.show_officials),
    path('rate_official/<str:name>/<str:elected_office>', views.rate_official),
    path('addRate/<str:name>/<str:elected_office>', views.addRate),
    path('rate/<str:name>/<str:elected_office>', views.rate_official),
    path('logout', views.logout),
    path('addOpinion/<str:name>/<str:elected_office>', views.addOpinion),
    path('opinion_official/<str:name>/<str:elected_office>', views.opinion_official),
    path('editOpinion/<int:opinion_id>', views.editOpinion),
    path('deleteOpinion/<int:opinion_id>', views.deleteOpinion),
    path('addReply/<str:name>/<str:elected_office>', views.addReply),
    path('opinion_official/<str:name>/<str:elected_office>', views.opinion_official),
    path('editOpinion/<int:opinion_id>', views.editOpinion),
    path('deleteOpinion/<int:opinion_id>', views.deleteOpinion),
    path('deleteReply/<int:reply_id>', views.deleteReply),
    path('users/', views.users),
    path('deleteUser/<int:user_id>', views.deleteUser),
    path('message', views.message, name='message-list'),
    path('comment', views.comment),
    path('deleteMessage/<int:message_id>', views.deleteMessage),
    path('deleteComment/<int:comment_id>', views.deleteComment),
    path('zipcode/', views.zipcode),
    # path('upload/', views.image_upload_view),
    path('editMessage/<int:message_id>', views.editMessage),
    path('updateMessage/<int:message_id>', views.updateMessage),
    path('editComment/<int:comment_id>', views.editComment),
    path('updateComment/<int:comment_id>', views.updateComment),
    path('deleteUser/<int:user_id>', views.deleteUser),
    path('editUser/<int:user_id>', views.editUser),
    path('like_message/', views.like_message, name="like-message"),
    path('like_comment/', views.like_comment, name="like-comment"),
    path('addMessage/', views.addMessage),
    path('profile/', views.profile),
]