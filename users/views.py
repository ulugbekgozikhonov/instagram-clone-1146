from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render


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


def signup_page(request):
	return render(request, "signup.html")
