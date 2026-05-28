import pytest
from django.urls import reverse
from .factories import BookFactory


@pytest.mark.django_db
def test_order_creation(client):
    book = BookFactory(price=20, stock=5)

    client.post(
        reverse("cart_add", args=[book.pk]),
        {"quantity": 1}
    )

    response = client.post(
        reverse("order_create"),
        {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "phone": "123456789",
            "address": "123 Main St"
        }
    )
    assert response.status_code in [301, 302]


@pytest.mark.django_db
def test_order_create_view_accessible(client):
    response = client.get(reverse("order_create"), follow=True)
    assert response.status_code == 200
