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


def test_book_update_view_requires_login(client):
    response = client.get(reverse('update_book', args=[1]))
    assert response.status_code in [301, 302]


def test_book_delete_view_requires_login(client):
    response = client.get(reverse('delete_book', args=[1]))
    assert response.status_code in [301, 302]


def test_cart_view_requires_login(client):
    response = client.get(reverse('cart_detail'))
    assert response.status_code in [301, 302]


@pytest.mark.django_db
def test_book_search_filter(client):
    response = client.get(reverse('books'), {'search': 'test'}, follow=True)
    assert response.status_code == 200


@pytest.mark.django_db
def test_book_price_filter(client):
    response = client.get(reverse('books'), {'min_price': 10, 'max_price': 50}, follow=True)
    assert response.status_code == 200


@pytest.mark.django_db
def test_books_list_with_pagination(client):
    response = client.get(reverse('books'), {'page': 1}, follow=True)
    assert response.status_code == 200


@pytest.mark.django_db
def test_books_list_with_ordering(client):
    response = client.get(reverse('books'), {'ordering': 'price'}, follow=True)
    assert response.status_code == 200
