import pytest
from books.models import Book, Category
from .factories import BookFactory, CategoryFactory


@pytest.mark.django_db
def test_category_creation():
    category = Category.objects.create(name="Fantasy", slug="fantasy")
    assert category.name == "Fantasy"
    assert str(category) == "Fantasy"


@pytest.mark.django_db
def test_book_creation():
    category = CategoryFactory(name="Sci-Fi")
    book = BookFactory(
        title="Dune",
        category=category,
        price=25.99,
        stock=10,
        is_active=True
    )
    assert book.title == "Dune"
    assert book.price == 25.99
    assert book.stock == 10
    assert book.is_active is True


@pytest.mark.django_db
def test_book_price_positive():
    category = CategoryFactory()
    book = BookFactory(category=category, price=15.50)
    assert book.price > 0


@pytest.mark.django_db
def test_book_stock_not_negative():
    category = CategoryFactory()
    book = BookFactory(category=category, stock=0)
    assert book.stock >= 0


@pytest.mark.django_db
def test_book_active_filter():
    category = CategoryFactory()
    active_book = BookFactory(category=category, is_active=True)
    inactive_book = BookFactory(category=category, is_active=False)

    active_books = Book.objects.filter(is_active=True)

    assert active_book in active_books
    assert inactive_book not in active_books