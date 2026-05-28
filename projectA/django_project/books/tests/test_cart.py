import pytest
from django.urls import reverse
from .factories import BookFactory


@pytest.mark.django_db
def test_cart_detail_empty(client):
    response = client.get(reverse("cart_detail"), follow=True)

    assert response.status_code == 200


@pytest.mark.django_db
def test_cart_add_redirects(client):
    book = BookFactory(stock=10, is_active=True)

    response = client.post(
        reverse("cart_add", args=[book.pk]),
        {"quantity": 1}
    )

    assert response.status_code in [301, 302]


@pytest.mark.django_db
def test_cart_add_out_of_stock(client):
    book = BookFactory(stock=0, is_active=True)

    response = client.post(
        reverse("cart_add", args=[book.pk]),
        {"quantity": 1}
    )

    assert response.status_code in [301, 302]


@pytest.mark.django_db
def test_cart_remove(client):
    book = BookFactory()

    client.post(
        reverse("cart_add", args=[book.pk]),
        {"quantity": 1}
    )

    response = client.post(reverse("cart_remove", args=[book.pk]))

    assert response.status_code in [301, 302]
