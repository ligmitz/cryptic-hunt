from django.db import models

# Create your models here.


class Level(models.Model):
	""" A model representing a single level """
	DEFAULT_LEVEL = 1
	
	level_id = models.AutoField(primary_key=True) 
	title = models.CharField(max_length=100)
	question = models.CharField(max_length=255)
	answer = models.CharField(max_length=120)
	hint = models.CharField(max_length=255, null=True, blank=True)
	
	image = models.ImageField(
			null = True,
			blank = True
		)

	def __str__(self):
		return self.title

