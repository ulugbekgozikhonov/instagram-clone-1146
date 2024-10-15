from django.db import models

from general.models import BaseModel
from users.models import User


# Post model
class Post(BaseModel):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
	image = models.ImageField(upload_to="posts/images/")
	caption = models.TextField(blank=True)

	def __str__(self):
		return f"{self.user.username} - {self.id}"


# Comment model
class Comment(BaseModel):
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	text = models.TextField()

	def __str__(self):
		return f"{self.user.username} - {self.text[:20]}"


# Like model
class Like(BaseModel):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')

	def __str__(self):
		return f"{self.user.username} liked {self.post.id}"


# Follower model
class Follower(BaseModel):
	user = models.ForeignKey(User, related_name="following", on_delete=models.CASCADE)
	follower = models.ForeignKey(User, related_name="followers", on_delete=models.CASCADE)
	followed_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.follower.username} follows {self.user.username}"