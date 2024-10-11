from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

EMAIL, PHONE_NUMBER = "EMAIL", "PHONE_NUMBER"


class GenderType(models.TextChoices):
	MALE = "MALE", "male"
	FEMALE = "FEMALE", "female"
	UNKNOWN = "UNKNOWN", "unknown"


class User(AbstractUser):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	phone_number = models.CharField(max_length=20, null=True, blank=True, unique=True)
	date_of_birth = models.DateField(null=True, blank=True)
	gender = models.CharField(max_length=7, choices=GenderType.choices, default=GenderType.UNKNOWN)
	avatar = models.ImageField(upload_to="users/avatars/", null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	email = models.EmailField(max_length=55, unique=True, blank=True, null=True)
	updated_at = models.DateTimeField(auto_now=True)
	login_type = models.CharField(max_length=31)

	def save(self, *args, **kwargs):
		pass
