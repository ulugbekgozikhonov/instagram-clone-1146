from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from .models import Post


@login_required
def post_page(request):
	user = request.user
	if request.method == "POST":
		post = request.FILES.get("post")
		caption = request.POST.get("caption")
		Post.objects.create(
			image=post,
			caption=caption,
			user=user
		)

		return HttpResponse("Created")

	posts = Post.objects.filter(user_id=user.id).order_by("-created_at").all()

	return render(request, "post.html", {"posts": posts})
