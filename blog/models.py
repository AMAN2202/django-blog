from django.db import models
from django.utils import timezone
from django.urls import reverse


class Post(models.Model):
    author = models.ForeignKey('auth.user', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.datetime.now())
    publish_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.publish_date = timezone.datetime.now()
        self.save()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_list')


class Comment(models.Model):
    post = models.ForeignKey('blog.Post', related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey('auth.user', on_delete=models.CASCADE)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.datetime.now())

    def __str__(self):
        return self.author

    def get_absolute_url(self):
        return reverse('home')
