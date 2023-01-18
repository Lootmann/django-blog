from django.contrib.auth import get_user_model

CustomUser = get_user_model()


def create_user(username: str, email: str, password: str) -> CustomUser:
    return CustomUser.objects.create(username=username, email=email, password=password)
