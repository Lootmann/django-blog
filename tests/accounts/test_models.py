import pytest
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


@pytest.mark.django_db
class TestCustomUserModel:
    @pytest.fixture(autouse=True)
    def initial(self):
        CustomUser.objects.create(
            username="testman",
            email="testman@example.com",
            password="testman123",
        )

    def test_model_is_created(self):
        users = CustomUser.objects.all()
        assert users.count() == 1
        assert users.first().username == "testman"
        assert users.first().email == "testman@example.com"
        assert users.first().is_superuser is False
        assert users.first().is_staff is False
        assert users.first().is_active is True


@pytest.mark.django_db
class TestCustomSuperuserModel:
    @pytest.fixture(autouse=True)
    def initial(self):
        CustomUser.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="admin123",
        )

    def test_model_is_created(self):
        users = CustomUser.objects.all()
        assert users.count() == 1
        assert users.first().username == "admin"
        assert users.first().email == "admin@example.com"
        assert users.first().is_superuser is True
        assert users.first().is_staff is True
        assert users.first().is_active is True
