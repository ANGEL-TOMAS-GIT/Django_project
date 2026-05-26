import factory
from books.models import Category, Book


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = "Fantasy"
    slug = "fantasy"


class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Book

    title = "LOTR"
    category = factory.SubFactory(CategoryFactory)
    price = 20
    stock = 5
