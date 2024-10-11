from django import forms

from users.models import User


# MODEL_FORM
# class SignUpForm(forms.ModelForm):
# 	class Meta:
# 		model = User
# 		fields = ["phone_number", "password", "first_name", "username"]


class SignUpForm(forms.Form):
	user_input = forms.CharField(max_length=55,
	                             widget=forms.TextInput(attrs={'placeholder': "email or phone number"}))
	password = forms.CharField(max_length=8,
	                           widget=forms.TextInput(attrs={'placeholder': "password"}))
	full_name = forms.CharField(max_length=70,
	                            widget=forms.TextInput(attrs={'placeholder': "full name"}))
	username = forms.CharField(min_length=3, max_length=20,
	                           widget=forms.TextInput(attrs={'placeholder': "username"}))
