import factory
from django.contrib.auth import get_user_model
from books.models import Category, Book


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    email = factory.Sequence(lambda n: f"user{n}@example.com")
    phone_number = factory.Sequence(lambda n: f"1000000{n:03d}")
    password = factory.PostGenerationMethodCall("set_password", "password")


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda n: f"Fantasy {n}")
    slug = factory.Sequence(lambda n: f"fantasy-{n}")


class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Book

    title = factory.Sequence(lambda n: f"LOTR {n}")
    slug = factory.Sequence(lambda n: f"lotr-{n}")
    category = factory.SubFactory(CategoryFactory)
    author = factory.SubFactory(UserFactory)
    book_author = "J. R. R. Tolkien"
    price = 20
    stock = 5
    is_active = True