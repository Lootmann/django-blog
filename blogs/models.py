from django.contrib.auth import get_user_model
from django.db import models


class Blog(models.Model):
    class Meta:
        db_table = "blogs"
        verbose_name = "blog"
        verbose_name_plural = "blogs"

    title = models.CharField(max_length=128, blank=False)
    # TODO: should markdownize
    content = models.TextField(blank=True)
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    is_public = models.BooleanField(default=False)
    clicked_count = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField(
        get_user_model(),
        related_name="blog_like",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def time_to_read(self) -> int:
        # how long it takes to read content
        return max(len(self.content) // 300, 1)

    def content_short(self) -> str:
        return self.content[:100]

    def number_of_likes(self) -> int:
        # NOTE: 全部のModelが一斉に取得しにいくので結構重い?
        return self.likes.count()

    def __str__(self) -> str:
        return self.title
