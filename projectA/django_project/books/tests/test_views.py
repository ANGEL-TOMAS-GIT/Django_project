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
    
    
@pytest.mark.django_db
def test_home_page_redirects(client):
    response = client.get(reverse('home'), follow=True)
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_book_view_requires_login(client):
    response = client.get(reverse('create_book'))
    assert response.status_code in [301, 302]
    
@pytest.mark.django_db
def test_manage_books_view_requires_login(client):
    response = client.get(reverse("manage_books"))
    assert response.status_code in [301, 302]
    
@pytest.mark.django_db
def test_book_detail_404(client):
    response = client.get(reverse("book_detail", args=[99999]), follow=True)
    assert response.status_code == 404
    