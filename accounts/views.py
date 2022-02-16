from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail.message import EmailMultiAlternatives
from django.shortcuts import  redirect, render
from django.utils.encoding import force_str, force_bytes
# from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from .forms import SignUpForm
from .tokens import account_activation_token
from django.core.mail import send_mail
from django.template.loader import get_template
from django.http import HttpResponse, request
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from questions.lib.actions import show_leaderboard
# Create your views here.


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
			user.profile.phoneNumber = form.cleaned_data.get('phoneNumber')
			user.is_active=False
			user.save()
			# raw_password = form.cleaned_data.get('password1')
			current_site = get_current_site(request)
			mail_subject = 'Activate your account.'
			username = form.cleaned_data.get('username')
			email = form.cleaned_data.get('email')
			htmly = get_template('email_template.html')
			cunt={
                    'username': username,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
}
			from_email, to = 'abhedya.iste@gmail.com', email
			html_content=htmly.render(cunt)
			msg=EmailMultiAlternatives(mail_subject, html_content, from_email, [to])
			msg.attach_alternative(html_content, "text/html")
			msg.send()
			messages.success(request, f'we have sent a confirmation email.' )
			return redirect('home')

	# Else return an empty form
	form = SignUpForm()
	context = {
		'form' : form,
	}
	return render(request,'register.html', context)

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, f'Your email has been verified. You can login now' )
        return redirect('rules')
    else:
        return HttpResponse('Activation link is invalid!')
    
    
    
def leaderboard(request):
	"""
	Returns the leadboard, sorted first with level (desc) then time (asc)
	"""
	active = show_leaderboard()

	queryset = User.objects.order_by('-profile__current_level','profile__current_level_time').exclude(is_staff=True)
	context = {
		'queryset' : queryset,
		'active': active,
	}

	return render(request, 'leaderboard.html', context)


def home(request):
	return render(request, 'home.html')

def rules(request):
	return render(request, 'rules.html')


