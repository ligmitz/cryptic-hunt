from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


# Import Model
from .models import Profile

class SignUpForm(UserCreationForm):
	"""
	A sign up form for a new user
	"""
	# Insitute Name
	institute = forms.CharField(max_length=255)

	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)
		# Making name required
		self.fields['email'].required = True
		self.fields['first_name'].required = True

	class Meta:
		model = User
		# The fields shown in the form
		fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'institute' )

	def clean_email(self):
		email = self.cleaned_data.get('email')
		try:
			match = User.objects.get(email=email)
			raise forms.ValidationError('This email address is already in use.')
		except User.DoesNotExist:
			return email
		return email

