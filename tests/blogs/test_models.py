import pytest
from django.urls import reverse

from blogs.models import Blog
from tests.factory import create_user


@pytest.mark.django_db
class TestBlogModel:
    @pytest.fixture(autouse=True)
    def initial(self, client):
        self.user = create_user("hoge", "hoge@email.com", "hoge-123")
        client.force_login(self.user)

        self.blog = Blog.objects.create(
            title="super book",
            content="""print(\"hello world :^)\")""",
            author=self.user,
            is_public=False,
        )

    def test_model_is_created(self):
        books = Blog.objects.all()
        assert books.count() == 1

        book = books.first()
        assert str(book) == "super book"
        assert book.title == "super book"
        assert book.content == 'print("hello world :^)")'
        assert book.is_public is False
        assert book.time_to_read() == 1

    def test_clicked_count(self, client):
        assert self.blog.clicked_count == 0

        client.get(reverse("blogs:detail", kwargs={"pk": self.blog.id}))
        client.get(reverse("blogs:detail", kwargs={"pk": self.blog.id}))
        client.get(reverse("blogs:detail", kwargs={"pk": self.blog.id}))
        client.get(reverse("blogs:detail", kwargs={"pk": self.blog.id}))
        self.blog.refresh_from_db()

        assert self.blog.clicked_count == 4

    def test_time_to_read(self):
        blog = Blog.objects.create(title="new book", content="0" * 300 * 3, author=self.user)
        assert blog.time_to_read() == 3

    def test_content_short(self):
        content = "0123456789" * 300
        blog = Blog.objects.create(title="new book", content=content, author=self.user)
        short = content[:100]
        assert blog.content_short() == short
