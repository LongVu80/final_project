from django.contrib import admin
from .models import Message, Like

admin.site.register(Message)
admin.site.register(Like)