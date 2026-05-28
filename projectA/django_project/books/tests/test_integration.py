import pytest
from django.urls import reverse
from .factories import BookFactory


@pytest.mark.django_db
def test_user_can_add_to_cart(client):
    book = BookFactory(
        price=20,
        stock=5,
        is_active=True
    )

    response = client.post(
        reverse("cart_add", args=[book.pk]),
        {"quantity": 1}
    )

    assert response.status_code in [301, 302]
