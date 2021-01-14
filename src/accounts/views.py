from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from django.urls import reverse

# Create your views here.

from .forms import SignUpForm

def register(request):
	"""
	Register View, creates new users
	"""
	if request.method == 'POST':
		""" A new form is submitted """

		# Get the form
		form = SignUpForm(request.POST)
		if form.is_valid():
			# If form is validated
			# Save the user, refresh the database, save the user profile
			user = form.save()
			user.refresh_from_db()  # load the profile instance created by the signal
			user.profile.institute = form.cleaned_data.get('institute')
			user.save()
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=user.username, password=raw_password)
			login(request, user)
			return redirect(reverse('hunt'))
		else:
			context = {
				'form' : form,
			}
			return render(request,'register.html', context)

	# Else return an empty form
	form = SignUpForm()
	context = {
		'form' : form,
	}

	return render(request,'register.html', context)


def leaderboard(request):
	"""
	Returns the leadboard, sorted first with level (desc) then time (asc)
	"""
	queryset = User.objects.order_by('-profile__current_level','profile__current_level_time')
	context = {
		'queryset' : queryset,
	}
	return render(request, 'leaderboard.html', context)


def home(request):
	return render(request, 'home.html')

def rules(request):
	return render(request, 'rules.html')