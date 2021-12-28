from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Level
from .forms import LevelForm
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.utils import timezone
from .decorators.hunt_is_active import hunt_is_active
from django.utils.decorators import method_decorator
import logging


from django.urls import reverse

logger = logging.getLogger("questions.view")
FINAL_LEVEL = 10

class Hunt(LoginRequiredMixin, View):
	""" The Game """
	login_url = '/login/'
	redirect_field_name = '/hunt/'

	# Form field for the level
	form_class = LevelForm


	@method_decorator(hunt_is_active)
	def get(self, request, *args, **kwargs):
		""" 
		GET Request 
		1. get the current user by the request.user
		2. find their current level and return the question accordingly
		"""
		cur_user = User.objects.get(id=request.user.id)
		if cur_user.profile.is_banned:
			return render(request,'home.html')

		cur_level = cur_user.profile.current_level
		user_is_cleared = cur_user.profile.is_cleared
		form = self.form_class()
		context = {
			'level': cur_level,
			'cleared': user_is_cleared,
			'form': form,
		}
		return render(request,'level.html',context)


	@method_decorator(hunt_is_active)
	def post(self,request, *args, **kwargs):
		"""
		POST request
		1. Get the current user and their answer
		2. If the answer is correct, update the level
		"""
		cur_user = User.objects.get(id=request.user.id)
		cur_level = cur_user.profile.current_level
		form = self.form_class(request.POST)
		if form.is_valid():
			ans = form.cleaned_data.get('answer')
			valid_answer = cur_level.answer.lower().split(",")
			if ans in valid_answer:
				logger.info("Levelcleared")
				messages.success(request, f"Level {cur_level.level_id} cleared")
				level_number = cur_user.profile.current_level.level_id
				
				if level_number == FINAL_LEVEL:
					cur_user.profile.is_cleared = True

				try:
					cur_user.profile.current_level = Level.objects.get(level_id = level_number + 1)
					cur_user.profile.current_level_time = timezone.now()
				except:
					pass
				cur_user.profile.save()
			else:
				messages.warning(request,"Wrong Answer")

		return redirect(reverse('hunt'))
