from django.contrib import admin

from .models import Group, Topic, Message

admin.site.register(Group)
admin.site.register(Topic)
admin.site.register(Message)