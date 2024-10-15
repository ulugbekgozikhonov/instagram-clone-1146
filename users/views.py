from django.contrib.auth import authenticate, login
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone

from users.forms import SignupForm
from users.models import User, EMAIL, PHONE_NUMBER, UserConfirmation
from users.service import check_email_or_phone


# MODEL_FORM
# def signup_page(request):
# 	if request.method == "POST":
# 		form = SignupForm(request.POST)
# 		if form.is_valid():
# 			form.save()
# 		return HttpResponse("successfully register")
# 	else:
# 		form = SignupForm()
# 		return render(request, "signup.html", {"form": form})

# FORM


def login_page(request):
	if request.method == "POST":
		user_inp = request.POST.get("user_inp")
		password = request.POST.get("password")
		user = authenticate(request, username=user_inp, password=password)
		if user is not None:
			login(request, user)
			return redirect("post:post")
		else:
			return HttpResponse("Login or password error")

	return render(request, "login.html")


def signup_page(request):
	if request.method == "POST":
		form = SignupForm(data=request.POST)
		if not form.is_valid():
			return HttpResponse("Invalid form data")

		user_inp = form.cleaned_data.get('user_input')
		username = form.cleaned_data.get('username')
		auth_type = check_email_or_phone(user_inp)

		if auth_type:
			if User.objects.filter(Q(email=user_inp) | Q(phone_number=user_inp), is_active=True).exists():
				return HttpResponse("This user already registered")

		if User.objects.filter(Q(username=username) & Q(is_active=True)).exists():
			return HttpResponse("This username is already taken")

		temp_user = User.objects.filter(Q(email=user_inp) | Q(phone_number=user_inp), is_active=False).first()

		if temp_user:
			print(username, "USERname")
			temp_user.username = username
			temp_user.first_name = form.cleaned_data.get("full_name")
			temp_user.set_password(form.cleaned_data.get("password"))
			temp_user.auth_type = auth_type
			temp_user.email = user_inp if auth_type == EMAIL else None
			temp_user.phone_number = user_inp if auth_type == PHONE_NUMBER else None
			temp_user.save()
		else:
			try:
				temp_user = User.objects.create_user(
					email=user_inp if auth_type == EMAIL else None,
					phone_number=user_inp if auth_type == PHONE_NUMBER else None,
					password=form.cleaned_data.get("password"),
					first_name=form.cleaned_data.get("full_name"),
					username=username,
					auth_type=auth_type,
					is_active=False
				)
			except Exception as e:
				return HttpResponse(f"Error: {str(e)}")

		request.session['temp_user_id'] = str(temp_user.id)
		return redirect('birth-date')

	form = SignupForm()
	return render(request, "signup.html", {"form": form})


def birth_date_page(request):
	temp_user_id = request.session.get('temp_user_id')

	if not temp_user_id:
		return HttpResponse("No user found in session!")

	if request.method == "POST":
		date_of_birth = request.POST.get("date_of_birth")
		temp_user = User.objects.get(id=temp_user_id)

		temp_user.date_of_birth = date_of_birth
		temp_user.save()

		verification_code = temp_user.create_verify_code(PHONE_NUMBER if temp_user.phone_number else EMAIL)

		if temp_user.phone_number:
			# send_sms(temp_user.phone_number, verification_code)
			pass
		elif temp_user.email:

			# send_email(temp_user.email, verification_code)
			print("CODE", verification_code)
			return render(request, 'email_confirmation.html')

	return render(request, 'birth_date.html')


def confirmation_code(request):
	temp_user_id = request.session.get('temp_user_id')

	if not temp_user_id:
		return HttpResponse("No user found in session!")

	if request.method == "POST":
		code = request.POST.get("code")
		user = User.objects.filter(id=temp_user_id).first()

		user_confirmation = UserConfirmation.objects.filter(
			Q(code=code) & Q(user_id=temp_user_id) & Q(is_confirmed=False)).last()
		if user_confirmation is None:
			return HttpResponse("Code is invalid")

		if timezone.now() <= user_confirmation.expire_time:
			user_confirmation.is_confirmed = True
			user_confirmation.save()
			user.is_active = True
			user.save()
			return redirect("login")

		else:
			return HttpResponse("expire time")
