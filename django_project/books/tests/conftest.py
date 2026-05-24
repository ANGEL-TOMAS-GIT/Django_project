import pytest
from django.contrib.auth.models import User
from books.models import Book, Category


# =========================
# CLIENT
# =========================

@pytest.fixture
def client():
    from django.test import Client
    return Client()


# =========================
# USER
# =========================

@pytest.fixture
def user():
    return User.objects.create_user(
        username="test_user",
        password="12345"
    )


# =========================
# CATEGORY
# =========================

@pytest.fixture
def category():
    return Category.objects.create(
        name="Fantasy",
        slug="fantasy"
    )


# =========================
# BOOK
# =========================

@pytest.fixture
def book(category):
    return Book.objects.create(
        title="LOTR",
        category=category,
        price=10,
        stock=5,
        is_active=True
    )
