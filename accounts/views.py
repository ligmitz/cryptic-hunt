from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.shortcuts import  render
from django.utils.encoding import force_str, force_bytes
# from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from .forms import SignUpForm
from .tokens import account_activation_token
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.http import HttpResponse
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
			message = render_to_string('email_template.html', {
                            'user': user,
                            'domain': current_site.domain,
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                            'token': account_activation_token.make_token(user),
                        })

			to_email = form.cleaned_data.get('email')
			send_mail(mail_subject, message, 'abhedya.iste@gmail.com', [to_email])
			return  HttpResponse('Please confirm your email address to complete the registration')
		# else:
  #      		 form = SignUpForm()
	 #         return render(request, 'register.html', {'form' : form})
			# user = authenticate(username=user.username, password=raw_password)
			# login(request, user)

            
			# return redirect(reverse('hunt'))
		# else:
		# 	context = {
		# 		'form' : form,
		# 	}
		# 	return render(request,'register.html', context)

	# Else return an empty form
	form = SignUpForm()
	context = {
		'form' : form,
	}

	return render(request,'register.html', context)

	# return render(request, 'user/login.html', {'form': form})


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
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
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
