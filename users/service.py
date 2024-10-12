import re

from users.models import EMAIL, PHONE_NUMBER

from django.core.mail import send_mail
from django.conf import settings

EMAIL_REGEX = r"[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+"
PHONE_NUMBER_REGEX = r'^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$'


def check_email_or_phone(user_inp):
	if re.match(EMAIL_REGEX, user_inp):
		return EMAIL
	elif re.match(PHONE_NUMBER_REGEX, user_inp):
		return PHONE_NUMBER
	else:
		return False


def send_email(to_whom, code):
	send_mail(
		'Instagram Code',
		f'Your verification code>>:{code}',
		settings.EMAIL_HOST_USER,
		[to_whom]
	)
