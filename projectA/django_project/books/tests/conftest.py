import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from books.models import Book, Category


def get_user_manager():
    User = get_user_model()
    return getattr(User, "objects", None) or getattr(User, "object")


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def user():
    manager = get_user_manager()
    return manager.create_user(
        email="test_user@example.com",
        phone_number="1112223333",
        password="12345"
    )


@pytest.fixture
def admin_user():
    manager = get_user_manager()
    return manager.create_superuser(
        email="admin@example.com",
        phone_number="9998887777",
        password="password"
    )


@pytest.fixture
def category():
    return Category.objects.create(
        name="Fantasy",
        slug="fantasy"
    )


@pytest.fixture
def book(category, user):
    return Book.objects.create(
        title="LOTR",
        slug="lotr",
        category=category,
        author=user,
        book_author="J. R. R. Tolkien",
        price=10,
        stock=5,
        is_active=True
    )