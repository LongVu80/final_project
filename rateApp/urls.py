from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('login/', views.login),
    path('register/', views.register),
    path('success/', views.success),
    path('view_officials', views.view_officials),
    path('show_officials/', views.show_officials),
    path('officials/', views.show_officials),
    path('rate_official/', views.rate_official),
    path('addRate/', views.addRate),
    path('rate/<str:name>/<str:elected_office>', views.rate_official),
    path('logout', views.logout),
    path('reply', views.reply),
    path('opinion', views.opinion),
    path('deleteReply/<int:reply_id>', views.deleteReply),
    path('deleteOpinion/<int:opinion_id>', views.deleteOpinion),
]