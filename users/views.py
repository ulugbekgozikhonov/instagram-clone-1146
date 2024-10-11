from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect

from users.forms import SignUpForm
from users.models import User, EMAIL
from users.service import check_email_or_phone


def login_page(request):
	if request.method == "POST":
		user_input = request.POST.get("user_input")
		password = request.POST.get("password")
		user = authenticate(request, username=user_input, password=password)

		if user is not None:
			login(request, user)
			return render(request, "home.html")
		else:
			return HttpResponse("login or password error")
	return render(request, "login.html")


# MODEL_FORM
# def signup_page(request):
# 	if request.method == "POST":
# 		form = SignUpForm(request.POST)
# 		if form.is_valid():
# 			form.save()
# 		return HttpResponse("successfully register")
# 	else:
# 		form = SignUpForm()
# 		return render(request, "signup.html", {"form": form})

# FORM
def signup_page(request):
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			user_inp = form.cleaned_data.get("user_input")
			username = form.cleaned_data.get("username")
			email_or_phone = check_email_or_phone(user_inp)
			password = form.cleaned_data.get("password")
			full_name = form.cleaned_data.get("full_name")
			if email_or_phone:
				if email_or_phone == EMAIL:
					try:
						user = User.objects.create(
							email=user_inp,
							first_name=full_name,
							password=password,
							username=username
						)

					except Exception as e:
						print(e)
						return HttpResponse(e)
				else:
					try:
						user = User.objects.create(
							phone_number=user_inp,
							first_name=full_name,
							password=password,
							username=username
						)

					except Exception as e:
						print(e)
						return HttpResponse(e)
				request.session["user_id"] = f"{user.id}"
			else:
				return HttpResponse("Siz email yoki telfon raqam kirtimadingiz")
		return redirect("birth-date")

	else:
		form = SignUpForm()
		return render(request, "signup.html", {"form": form})


def birth_date_page(request):
	return render(request, "birth_date.html", {"user": request.session.get("user_id")})
