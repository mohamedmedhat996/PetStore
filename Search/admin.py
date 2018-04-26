from django.contrib import admin

# Register your models here.
from Search.models import RecentSearch, Comment

admin.site.register(RecentSearch)
admin.site.register(Comment)
