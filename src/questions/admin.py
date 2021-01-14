from django.contrib import admin

# Register your models here.
from .models import Level

class LevelModelAdmin(admin.ModelAdmin):
	""" Admin Model """

	# Things to display
	list_display = ["level_id", "title", "question"]

	# Search Fields
	search_fields = ["level_id", "question"]

	# Meta
	class Meta:
		model = Level

admin.site.register(Level, LevelModelAdmin)