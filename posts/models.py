"""
Module containing models for the Post app.
"""
from django.db import models
from django.utils.text import slugify
from django.conf import settings


# Create your models here.
class Post(models.Model):
    """
    Model representing Post information.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/%y/%m/%d')
    caption = models.TextField(blank=True)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    liked_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='posts_liked',
        blank=True
    )

    objects = models.Manager()

    @property
    def other_likes_count(self):
        """
        Returns the number of users who liked the post,
        excluding the first displayed user.
        """
        return max(self.liked_by.count() - 1, 0)

    def __str__(self):
        """
        Return a string representation of the Post.
        """
        return str(self.title)

    def save(self, *args, **kwargs):
        """
        Saves slug for the post.
        """
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Comment(models.Model):
    """
    Model representing comment information.
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comment')
    body = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now=True)
    posted_by = models.CharField(max_length=200)

    objects = models.Manager()

    class Meta:
        """
        Metadata for the Comment.

        Specifies the associated Comment in order of created timestamp.
        """
        ordering = ('created',)

    def __str__(self):
        """
        Return a string representation of the Comment.
        """
        return str(self.body)