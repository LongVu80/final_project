from django.contrib import admin
from .models import Message, Like, User

admin.site.register(Message)
admin.site.register(Like)
admin.site.register(User)