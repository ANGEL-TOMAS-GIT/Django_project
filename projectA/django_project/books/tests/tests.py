from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from books.models import Book, Category


User = get_user_model()


def create_test_user(email, phone_number, password):
    manager = getattr(User, "objects", None) or getattr(User, "object")
    return manager.create_user(
        email=email,
        phone_number=phone_number,
        password=password
    )


class BookModelTest(TestCase):
    def setUp(self):
        self.user = create_test_user(
            email='test@test.com',
            phone_number='1234567890',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )

    def test_create_book(self):
        book = Book.objects.create(
            category=self.category,
            title='Test Book',
            slug='test-book',
            book_author='Test Author',
            author=self.user,
            price=19.99,
            stock=5
        )

        self.assertEqual(book.title, 'Test Book')
        self.assertEqual(book.book_author, 'Test Author')
        self.assertEqual(book.author, self.user)
        self.assertEqual(float(book.price), 19.99)

    def test_book_str(self):
        book = Book.objects.create(
            category=self.category,
            title='My Book',
            slug='my-book',
            book_author='My Author',
            author=self.user,
            price=10.00,
            stock=3
        )

        self.assertIn('My Book', str(book))


class BookAPITest(APITestCase):
    def setUp(self):
        self.user = create_test_user(
            email='api@test.com',
            phone_number='0987654321',
            password='apipass123'
        )
        self.client.force_authenticate(user=self.user)

    def test_list_books(self):
        url = reverse('books')
        response = self.client.get(url, follow=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
