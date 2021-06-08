from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('login/', views.login),
    path('register/', views.register),
    path('success/', views.success),
    path('view-officials', views.view_officials),
    path('show-officials', views.show_officials),
    path('rate/', views.rate),
    path('rate/<str:name>/<str:elected_office>', views.rate_official),
    path('logout', views.logout),
    path('reply', views.reply),
    path('opinion', views.opinion),
    path('deleteReply/<int:reply_id>', views.deleteReply),
    path('deleteOpinion/<int:opinion_id>', views.deleteOpinion),
]