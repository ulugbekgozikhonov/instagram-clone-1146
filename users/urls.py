from django.urls import path
from .views import login_page, signup_page, birth_date_page, confirmation_code

app_name = "user"

urlpatterns = [
	path('', login_page, name='login'),
	path('signup/', signup_page, name='signup'),
	path('birth-date/', birth_date_page, name='birth-date'),
	path('confirmation-code/', confirmation_code, name='confirmation'),
]
