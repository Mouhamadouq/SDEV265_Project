from django.conf import settings
from django.db import models
from django.utils import timezone

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    @property
    def upvotes_count(self):
        return self.upvotes.count()

    @property
    def downvotes_count(self):
        return self.downvotes.count()


class Upvote(models.Model):
    post = models.ForeignKey(Post, related_name='upvotes', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('post', 'user')


class Downvote(models.Model):
    post = models.ForeignKey(Post, related_name='downvotes', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('post', 'user')