import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from books.models import Book, Category


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def user():
    User = get_user_model()
    manager = getattr(User, "objects", None) or getattr(User, "object")

    return manager.create_user(
        email="test_user@example.com",
        phone_number="1112223333",
        password="12345"
    )


@pytest.fixture
def category():
    return Category.objects.create(
        name="Fantasy",
        slug="fantasy"
    )


@pytest.fixture
def book(category):
    return Book.objects.create(
        title="LOTR",
        category=category,
        price=10,
        stock=5,
        is_active=True
    )