import pytest
from django.urls import reverse
from books.models import Book, Category
from .factories import BookFactory, CategoryFactory


@pytest.mark.django_db
def test_order_creation(client):
    category = CategoryFactory()
    book = BookFactory(category=category, price=20, stock=5)

    # Add to cart
    client.post(reverse("cart_add", args=[book.pk]), {"quantity": 1})

    response = client.post(reverse("order_create"), {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "phone": "123456789",
        "address": "123 Main St"
    })

    assert response.status_code in [200, 302]


@pytest.mark.django_db
def test_order_list_view(client, admin_user):
    client.force_login(admin_user)
    response = client.get(reverse("order_list"))
    assert response.status_code == 200
    