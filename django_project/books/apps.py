from django.apps import AppConfig


class BooksConfig(AppConfig):
    name = 'books'

    def ready(self) -> None:
        import books.signals # noqa
