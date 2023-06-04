from django.db import models
from django.contrib.auth.models import User


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    ``created_at`` and ``updated_at`` fields.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# Create your models here.
class Category(TimeStampedModel):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


STATUS_CHOICE = (("Draft", "Draft"), ("Published", "Published"))


class Blog(TimeStampedModel):
    title = models.CharField(max_length=500)
    slug = models.SlugField(max_length=500, unique=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="blogs"
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    featured_image = models.ImageField(upload_to="uploads/%Y/%m/%d")
    short_description = models.TextField(max_length=2000)
    blog_body = models.TextField(max_length=5000)
    status = models.CharField(max_length=20, choices=STATUS_CHOICE, default="Draft")
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class About(models.Model):
    header = models.CharField(max_length=50)
    description = models.TextField(max_length=2000)

    class Meta:
        verbose_name_plural = "About"

    def __str__(self):
        return self.header


class SocialLink(models.Model):
    social_name = models.CharField(max_length=20)
    social_url = models.URLField()

    def __str__(self):
        return self.social_name


class Comment(TimeStampedModel):
    blog_post = models.ForeignKey(Blog, on_delete=models.CASCADE)
    commented_by = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField(max_length=2000)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies"
    )

    def __str__(self):
        return self.comment_text
