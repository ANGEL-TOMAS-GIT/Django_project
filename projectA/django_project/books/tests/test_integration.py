import pytest
from django.urls import reverse
from books.models import Book, Category


@pytest.mark.django_db
def test_user_can_add_to_cart(client):
    cat = Category.objects.create(
        name="Fantasy",
        slug="fantasy"
    )

    book = Book.objects.create(
        title="LOTR",
        category=cat,
        price=20,
        stock=5,
        is_active=True
    )

    response = client.post(
        reverse("cart_add", args=[book.pk]),
        {"quantity": 1}
    )

    assert response.status_code == 302
