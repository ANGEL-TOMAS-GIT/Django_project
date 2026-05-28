import pytest
from django.urls import reverse
from .factories import BookFactory


@pytest.mark.django_db
def test_books_list(client):
    response = client.get(reverse("books"), follow=True)

    assert response.status_code == 200


@pytest.mark.django_db
def test_book_detail(client):
    book = BookFactory(
        title="Harry Potter",
        stock=2
    )

    response = client.get(
        reverse("book_detail", args=[book.pk]),
        follow=True
    )

    assert response.status_code == 200


@pytest.mark.django_db
def test_book_str():
    book = BookFactory(title="Harry Potter")

    assert "Harry Potter" in str(book)