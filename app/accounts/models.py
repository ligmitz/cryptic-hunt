from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.db import models

from questions.models import Level
# Create your models here.

class Profile(models.Model):
	""" A Model Representing a User """

	user = models.OneToOneField(User, on_delete = models.CASCADE)
	institute = models.CharField(max_length=255, null=True)
	phoneNumber = models.IntegerField(default=0)
	current_level = models.ForeignKey(Level, default = Level.DEFAULT_LEVEL,on_delete=models.CASCADE)
	current_level_time = models.DateTimeField(default=timezone.now)
	is_banned = models.BooleanField(default = False)
	is_admin = models.BooleanField(default = False)
	is_cleared = models.BooleanField(default=False)

	def __str__(self):
		return self.user.username

	def get_level(self):
		"""
		Returns the current level of the user
		"""
		return self.current_level.level_id

	def get_name(self):
		"""
		Returns the name of the user
		"""
		return self.user.first_name + " " + self.user.last_name

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
	"""
	Creates a user profile just after a user is created
	"""
	if created:
		Profile.objects.create(user=instance)
	instance.profile.save()