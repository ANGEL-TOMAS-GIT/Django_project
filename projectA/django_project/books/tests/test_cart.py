import pytest
from django.urls import reverse
from .factories import BookFactory, CategoryFactory


@pytest.mark.django_db
def test_cart_detail_empty(client):
    response = client.get(reverse("cart_detail"))
    assert response.status_code == 200
    assert response.context["cart"] == {}


@pytest.mark.django_db
def test_cart_add_redirects(client):
    category = CategoryFactory()
    book = BookFactory(category=category, stock=10, is_active=True)

    response = client.post(reverse("cart_add", args=[book.pk]), {"quantity": 1})

    assert response.status_code == 302
    assert response.url == reverse("cart_detail")


@pytest.mark.django_db
def test_cart_add_out_of_stock(client):
    category = CategoryFactory()
    book = BookFactory(category=category, stock=0, is_active=True)

    response = client.post(reverse("cart_add", args=[book.pk]), {"quantity": 1})

    assert response.status_code == 302


@pytest.mark.django_db
def test_cart_remove(client):
    category = CategoryFactory()
    book = BookFactory(category=category)

    # Add to cart first
    client.post(reverse("cart_add", args=[book.pk]), {"quantity": 1})

    # Remove from cart
    response = client.post(reverse("cart_remove", args=[book.pk]))

    assert response.status_code == 302