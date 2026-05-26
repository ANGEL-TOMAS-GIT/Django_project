import pytest
from django.urls import reverse
from books.models import Book, Category
from .factories import BookFactory


@pytest.mark.django_db
def test_books_list(client):
    response = client.get(reverse("books"))

    assert response.status_code == 200


@pytest.mark.django_db
def test_book_detail(client):
    cat = Category.objects.create(name="Fantasy", slug="fantasy")

    book = Book.objects.create(
        title="Harry Potter",
        category=cat,
        price=20,
        stock=2
    )

    response = client.get(
        reverse("book_detail", args=[book.pk])
    )

    assert response.status_code == 200


@pytest.mark.django_db
def test_book_str():
    book = BookFactory(title="Harry Potter")
    assert "Harry Potter" in str(book)
