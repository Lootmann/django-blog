import pytest
from django.urls import reverse
from pytest_django import asserts

from blogs.models import Blog
from tests.factory import create_user


@pytest.mark.django_db
class TestPagesIndexView:
    @pytest.fixture(autouse=True)
    def initial(self, client):
        self.url = reverse("pages:index")
        self.response = client.get(self.url)

    def test_status_code(self):
        assert self.response.status_code == 200

    def test_templates_used(self):
        asserts.assertTemplateUsed(self.response, "base.html")
        asserts.assertTemplateUsed(self.response, "pages/index.html")

    def test_contains(self):
        asserts.assertContains(self.response, "pages/index.html")


@pytest.mark.django_db
class TestPagesIndexViewHasSomeBlogs:
    @pytest.fixture(autouse=True)
    def initial(self, client):
        user = create_user(username="hoge", email="hoge@email.com", password="hogehoge123")
        Blog.objects.create(title="blog 1", content="blog 1 hoge", is_public=True, author=user)

        user = create_user(username="hage", email="hage@email.com", password="hagehage123")
        Blog.objects.create(title="blog 2", content="blog 2 hoge", is_public=False, author=user)

        self.url = reverse("pages:index")
        self.response = client.get(self.url)

    def test_contains(self):
        asserts.assertContains(self.response, "@hoge")
        asserts.assertContains(self.response, "blog 1")
        asserts.assertContains(self.response, "blog 1 hoge")

        asserts.assertNotContains(self.response, "@hage")
        asserts.assertNotContains(self.response, "blog 2")
        asserts.assertNotContains(self.response, "blog 2 hage")
