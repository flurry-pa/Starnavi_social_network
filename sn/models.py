from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# Fields are: date_joined, dislike, email, first_name, groups, id, is_active, is_staff, is_superuser,
#             last_login, last_name, like, logentry, password, post, user_permissions, username


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Like(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'post'],
                name='unique_like'
            ),
        ]


class Dislike(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'post'],
                name='unique_dislike'
            ),
        ]


class Analytics(models.Model):
    like_amount = models.CharField(max_length=64, default='-')      # PositiveIntegerField()
    date_from = models.DateField()
    date_to = models.DateField()


class UserActivity(models.Model):
    user_list = models.CharField(max_length=255, default=0)
    last_login = models.CharField('Last join or login', max_length=64)
    last_request = models.CharField('Last request (post or like)', max_length=64)
