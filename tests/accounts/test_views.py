import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from pytest_django import asserts

from accounts.forms import CustomUserCreationForm


@pytest.mark.django_db
class TestSignupViewGet:
    @pytest.fixture(autouse=True)
    def initial(self, client):
        url = reverse("accounts:signup")
        self.response = client.get(url)

    def test_template_used(self):
        asserts.assertTemplateUsed(self.response, "base.html")
        asserts.assertTemplateUsed(self.response, "registration/signup.html")


@pytest.mark.django_db
class TestSignupViewPost:
    @pytest.fixture(autouse=True)
    def initial(self, client):
        self.url = reverse("accounts:signup")

    def test_before_user_created(self):
        assert get_user_model().objects.count() == 0

    def test_template_used(self, client):
        data = {
            "username": "guest",
            "email": "guest@email.com",
            "password1": "admin123@you",
            "password2": "admin123@you",
        }
        response = client.post(self.url, data)
        asserts.assertRedirects(response, reverse("login"))

        assert get_user_model().objects.count() == 1


@pytest.mark.django_db
class TestSignupViewForm:
    @pytest.fixture(autouse=True)
    def initial(self, client):
        url = reverse("accounts:signup")
        self.response = client.get(url)

    def test_form(self):
        form = self.response.context.get("form")
        assert isinstance(form, CustomUserCreationForm)
        asserts.assertContains(self.response, "csrfmiddlewaretoken")
