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
    assert float(book.price) == 25.99
    assert book.stock == 10
    assert book.is_active is True


@pytest.mark.django_db
def test_book_price_positive():
    book = BookFactory(price=15.50)

    assert book.price > 0


@pytest.mark.django_db
def test_book_stock_not_negative():
    book = BookFactory(stock=0)

    assert book.stock >= 0


@pytest.mark.django_db
def test_book_active_filter():
    active_book = BookFactory(is_active=True, stock=5)
    inactive_book = BookFactory(is_active=False, stock=5)

    active_books = Book.objects.filter(is_active=True)

    assert active_book in active_books
    assert inactive_book not in active_books