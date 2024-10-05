from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from users.models import User


class CustomAuthBackend(ModelBackend):
	def authenticate(self, request, username=None, password=None, **kwargs):
		try:
			user = User.objects.filter(Q(username=username) | Q(phone_number=username) | Q(email=username)).first()
		except User.DoesNotExist:
			return None

		if user and user.check_password(password):
			return user
		return None
