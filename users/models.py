import random
import uuid
from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone

from general.models import BaseModel

EMAIL, PHONE_NUMBER = "EMAIL", "PHONE_NUMBER"


class GenderType(models.TextChoices):
	MALE = "MALE", "Male"
	FEMALE = "FEMALE", "Female"
	UNKNOWN = "UNKNOWN", "Unknown"


class User(AbstractUser, BaseModel):
	AUTH_TYPES = (
		(EMAIL, "Email"),
		(PHONE_NUMBER, "Phone Number")
	)

	phone_number = models.CharField(max_length=31, null=True, blank=True, unique=True)
	email = models.EmailField(max_length=100, unique=True, blank=True, null=True)
	date_of_birth = models.DateField(null=True, blank=True)
	avatar = models.ImageField(upload_to="users/avatars/", null=True, blank=True,
	                           validators=[FileExtensionValidator(allowed_extensions=['jpeg', 'jpg', 'png'])])
	gender = models.CharField(max_length=7, choices=GenderType.choices, default=GenderType.UNKNOWN)
	auth_type = models.CharField(max_length=33, choices=AUTH_TYPES)

	def __str__(self):
		return self.username

	def create_verify_code(self, verify_type):
		code = "".join([str(random.randint(0, 10)) for _ in range(6)])
		UserConfirmation.objects.create(
			user=self,
			verify_type=verify_type,
			code=code
		)
		print("USER CODE", code)
		return code


EXPIRE_TIME = 2


class UserConfirmation(models.Model):
	VERIFY_TYPE_CHOICES = (
		(PHONE_NUMBER, "Phone Number"),
		(EMAIL, "Email")
	)

	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	code = models.CharField(max_length=6)
	verify_type = models.CharField(max_length=31, choices=VERIFY_TYPE_CHOICES)
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="verify_codes")
	expire_time = models.DateTimeField(null=True)
	is_confirmed = models.BooleanField(default=False)

	def __str__(self):
		return f"{self.user.username} - {self.code}"

	def save(self, *args, **kwargs):
		self.expire_time = timezone.now() + timedelta(minutes=EXPIRE_TIME)
		super(UserConfirmation, self).save(*args, **kwargs)
