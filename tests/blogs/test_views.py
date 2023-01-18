import pytest
from django.urls import reverse
from pytest_django import asserts

from blogs.models import Blog
from tests.factory import create_user


@pytest.mark.django_db
class TestBlogsIndexView:
    @pytest.fixture(autouse=True)
    def initial(self, client):
        user = create_user("hoge", "hoge@email.com", "hoge@123")
        client.force_login(user)

        Blog.objects.create(
            title="Django Book",
            content="There is no there, there.",
            author=user,
            is_public=False,
        )

        user = create_user("hage", "hage@email.com", "hage@123")
        Blog.objects.create(
            title="hage book",
            content="I AM NOT HAGE",
            author=user,
            is_public=True,
        )

        self.url = reverse("blogs:index")
        self.response = client.get(self.url)

    def test_status_code(self):
        assert self.response.status_code == 200

    def test_template_used(self):
        asserts.assertTemplateUsed(self.response, "base.html")
        asserts.assertTemplateUsed(self.response, "blogs/index.html")

    def test_contains(self):
        asserts.assertContains(self.response, "blogs/index.html")
        asserts.assertContains(self.response, "@hoge")
        asserts.assertContains(self.response, "Django Book")
        asserts.assertContains(self.response, "There is no there, there.")

        asserts.assertNotContains(self.response, "@hage")
        asserts.assertNotContains(self.response, "hage book")
        asserts.assertNotContains(self.response, "I AM NOT HAGE")


@pytest.mark.django_db
class TestBlogsCreateView:
    @pytest.fixture(autouse=True)
    def initial(self, client, django_user_model):
        user = django_user_model.objects.create(
            username="test",
            email="test@example.com",
            password="admin@123",
        )
        client.force_login(user)

        url = reverse("blogs:create")
        data = {
            "title": "new book",
            "content": "This has no contents.",
        }
        self.response = client.post(url, data)

    def test_status_code(self):
        asserts.assertRedirects(self.response, reverse("blogs:index"), status_code=302)

    def test_model_is_created(self):
        blogs = Blog.objects.all()
        assert blogs.count() == 1

        assert blogs.first().title == "new book"
        assert blogs.first().content == "This has no contents."
        assert blogs.first().is_public is not True


@pytest.mark.django_db
class TestBlogsDetailView:
    @pytest.fixture(autouse=True)
    def initial(self, client):
        user = create_user("hoge", "hoge@email.com", "hage@123")
        client.force_login(user)
        self.blog = Blog.objects.create(
            title="new blog",
            content="Hi :^)",
            author=user,
        )
        self.url = reverse("blogs:detail", kwargs={"pk": self.blog.id})
        self.response = client.get(self.url)

    def test_status_code(self):
        assert self.response.status_code == 200

    def test_template_used(self):
        asserts.assertTemplateUsed(self.response, "base.html")
        asserts.assertTemplateUsed(self.response, "blogs/detail.html")

    def test_contains(self):
        asserts.assertContains(self.response, "new blog")
        asserts.assertContains(self.response, "Hi :^)")


@pytest.mark.django_db
class TestBlogsUpdateView:
    @pytest.fixture(autouse=True)
    def initial(self, client):
        user = create_user("hoge", "hoge@email.com", "hage@123")
        client.force_login(user)
        self.blog = Blog.objects.create(title="new blog", content="Hi :^)", author=user)

    def test_model_is_created(self):
        blogs = Blog.objects.all()
        assert blogs.count() == 1
        assert blogs.first().title == "new blog"
        assert blogs.first().content == "Hi :^)"

    def test_updated(self, client):
        url = reverse("blogs:update", kwargs={"pk": self.blog.id})
        response = client.post(url, {"title": "updated blog", "content": "Hello :D"})
        asserts.assertRedirects(response, reverse("blogs:detail", kwargs={"pk": self.blog.id}))

        blog = Blog.objects.first()
        assert blog.title == "updated blog"
        assert blog.content == "Hello :D"


@pytest.mark.django_db
class TestBlogsDeleteView:
    @pytest.fixture(autouse=True)
    def initial(self, client):
        user = create_user("hoge", "hoge@email.com", "hage@123")
        client.force_login(user)
        self.blog = Blog.objects.create(title="new blog", content="Hi :^)", author=user)
        self.url = reverse("blogs:delete", kwargs={"pk": self.blog.id})

    def test_model_is_created(self):
        blogs = Blog.objects.all()
        assert blogs.count() == 1
        assert blogs.first().title == "new blog"
        assert blogs.first().content == "Hi :^)"

    def test_deleted(self, client):
        response = client.post(self.url)
        asserts.assertRedirects(response, reverse("blogs:index"))

        blogs = Blog.objects.all()
        assert blogs.count() == 0

    def test_status_code(self, client):
        response = client.get(self.url)
        assert response.status_code == 200
        asserts.assertTemplateUsed(response, "base.html")
        asserts.assertTemplateUsed(response, "blogs/delete.html")
        asserts.assertContains(response, f"Are you sure Delete `{self.blog.title}`?")
        asserts.assertContains(response, f"{self.blog.title}")
        asserts.assertContains(response, f"{self.blog.content}")


@pytest.mark.django_db
class TestBlogsDeleteViewValidation:
    @pytest.fixture(autouse=True)
    def initial(self, client):
        user = create_user("test", "test@email.com", "testman123")
        client.force_login(user)
        self.blog = Blog.objects.create(title="new blog", content="blog content", author=user)

    def test_wrong_id_blog(self, client):
        # specifies wrong blog id
        url = reverse("blogs:delete", kwargs={"pk": self.blog.id + 100})
        response = client.get(url)
        asserts.assertTemplateUsed(response, "404.html")

    def test_try_to_delete_blog_by_wrong_user(self, client):
        client.logout()
        user = create_user("bot", "bot@email.com", "bot@123")
        client.force_login(user)
        url = reverse("blogs:delete", kwargs={"pk": self.blog.id})
        response = client.get(url)
        asserts.assertTemplateUsed(response, "404.html")


@pytest.mark.django_db
class TestDifferentAccountEdit:
    """
    create blogs by user1 and user2, try to edit user1 blog by user2
    this process should NOT be allowed by default
    """

    @pytest.fixture(autouse=True)
    def initial(self, client):
        self.user1 = create_user("user1", "user1@email.com", "user1user1")
        client.force_login(self.user1)
        self.blog1 = Blog.objects.create(title="I'm user1", content="hoge", author=self.user1)
        client.logout()

        self.user2 = create_user("user2", "user2@email.com", "user2user2")
        client.force_login(self.user2)
        self.blog2 = Blog.objects.create(title="I'm user2", content="hoge", author=self.user2)
        client.logout()

    def test_update_another_authors_blog(self, client):
        """
        currently logged in by user2
        created by user1, but edited by user2
        """
        client.force_login(self.user2)
        # self.blog1 author is user1
        url = reverse("blogs:update", kwargs={"pk": self.blog1.id})
        response = client.post(url, data={"title": "updated by user1"})
        asserts.assertTemplateUsed(response, "404.html")


@pytest.mark.django_db
class TestBlogLike:
    """
    create blogs by user1 and user2, try to edit user1 blog by user2
    this process should NOT be allowed by default
    """

    @pytest.fixture(autouse=True)
    def initial(self, client):
        self.user1 = create_user("user1", "user1@email.com", "user1user1")
        self.blog1 = Blog.objects.create(title="I'm user1", content="hoge", author=self.user1)

        self.user2 = create_user("user2", "user2@email.com", "user2user2")
        self.blog2 = Blog.objects.create(title="I'm user2", content="hoge", author=self.user2)
        client.force_login(self.user1)

    def test_status_code(self, client):
        def access_to_like(cl, blog_id):
            cl.get(reverse("blogs:toggle_like", kwargs={"blog_id": blog_id}))

        # user1 likes blog1, blog1 is liked by user1
        access_to_like(client, self.blog1.id)
        assert self.blog1.likes.all().count() == 1
        assert self.blog1.number_of_likes() == 1

        # user1 likes blog2, blog2 is liked by user1
        access_to_like(client, self.blog2.id)
        assert self.blog2.likes.all().count() == 1
        assert self.blog2.number_of_likes() == 1

        # user2 likes blog1, blog1 is liked by user1, user2
        client.force_login(self.user2)
        access_to_like(client, self.blog1.id)
        assert self.blog1.likes.all().count() == 2
        assert self.blog1.number_of_likes() == 2

        # user1 dislike blog1, blog1 is liked by user2
        client.force_login(self.user1)
        access_to_like(client, self.blog1.id)
        assert self.blog1.likes.all().count() == 1
        assert self.blog1.number_of_likes() == 1

        # user2 dislike blog1, then nobody likes blog1
        client.force_login(self.user2)
        access_to_like(client, self.blog1.id)
        assert self.blog1.likes.all().count() == 0
        assert self.blog1.number_of_likes() == 0
