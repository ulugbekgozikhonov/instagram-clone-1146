from django.contrib import admin
from .models import User, UserConfirmation


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
	list_display = ["id", "username"]


@admin.register(UserConfirmation)
class UserConfirmationAdmin(admin.ModelAdmin):
	list_display = ["code", "user"]

