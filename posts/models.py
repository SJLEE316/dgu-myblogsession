from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=50, null=False)
    content = models.TextField()
    view_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)
    image = models.ImageField(upload_to='images/', null=True)
    user = models.ForeignKey(User, on_delete = models.CASCADE, null=True)
    like_user_set = models.ManyToManyField(User, blank=True, related_name='like_user_set', through='Like') 
    #좋아요가 없어도 문제ㄴㄴ-> True, through는 중간에 Like가 있다. (중간다리)

    @property #좋아요 몇 개?
    def like_count(self):
        return self.like_user_set.count()


class Comment(models.Model): #1대N관계
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)
    writer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name='comments')

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (('user','post'))  #unique한 관계. 중복되는 것이 없다