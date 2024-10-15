from .views import post_page
from django.urls import path

app_name = "post"

urlpatterns = [
	path("post/", post_page, name="post")
]
