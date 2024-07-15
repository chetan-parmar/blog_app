import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from blog.manager import UserManager


class TimestampedModel(models.Model):
    """
    Abstract base model that provides self-updating
    'created_at' and 'updated_at' fields.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser, TimestampedModel):
    """
    Custom User model using email as the unique identifier instead of username.
    """

    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    username = None
    email = models.EmailField(unique=True, db_index=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        indexes = [
            models.Index(fields=["email", "is_active"]),
        ]

    def __str__(self):
        return self.email


class Category(TimestampedModel):
    """
    Category model for blog post classification.
    """

    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=100, db_index=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=["name"]),
        ]
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Post(TimestampedModel):
    """
    BlogPost model representing individual blog entries.
    """

    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    title = models.CharField(max_length=200, db_index=True)
    content = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="post_auther"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="post_category",
    )

    class Meta:
        indexes = [
            models.Index(fields=["title", "created_at"]),
            models.Index(fields=["author", "created_at"]),
            models.Index(fields=["category", "created_at"]),
        ]

    def can_edit(self, user):
        return self.author == user or user.is_superuser

    def __str__(self):
        return self.title


class Comment(TimestampedModel):
    """
    Comment model representing comments made on blog posts.
    """

    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments"
    )
    name = models.CharField(max_length=255)
    body = models.TextField()

    class Meta:
        indexes = [
            models.Index(fields=["post", "created_at"]),
            models.Index(fields=["name", "created_at"]),
        ]

    def __str__(self):
        return f"Comment by {self.name} on {self.post}"
