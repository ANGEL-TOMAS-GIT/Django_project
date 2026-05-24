import pytest
from books.models import Book, Category
from django.test import TestCase


class TestModel(TestCase):

    @pytest.mark.django_db
    def test_book_str(self):
        cat = Category.objects.create(name="Fantasy", slug="fantasy")

        book = Book.objects.create(
            title="LOTR",
            category=cat,
            price=10,
            stock=5
        )

        assert "LOTR" in str(book)

    @pytest.mark.django_db
    def test_default_photo(self):
        cat = Category.objects.create(name="SciFi", slug="scifi")

        book = Book.objects.create(
            title="Dune",
            category=cat,
            price=15,
            stock=3
        )
        assert book.get_photo_url()
