from django.contrib import admin

# Register your models here.
from .models import Profile

class ProfileAdminModel(admin.ModelAdmin):
	""" Admin Model """

	list_display = ["user" ,"current_level", "is_banned", "institute", "phoneNumber"]

	search_fields = ["user", "user.email"]

	ordering = ["-current_level", "current_level_time"]

	class Meta:
		model = Profile

admin.site.register(Profile, ProfileAdminModel)