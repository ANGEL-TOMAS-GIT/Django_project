from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from books.models import Book

User = get_user_model()

class BookModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )
    
    def test_create_book(self):
        book = Book.objects.create(
            title='Test Book',
            author='Test Author',
            price=19.99,
            created_by=self.user
        )
        self.assertEqual(book.title, 'Test Book')
        self.assertEqual(book.price, 19.99)
    
    def test_book_str(self):
        book = Book.objects.create(
            title='My Book',
            author='My Author',
            price=10.00,
            created_by=self.user
        )
        self.assertEqual(str(book), 'My Book')

class BookAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='apiuser',
            password='apipass123'
        )
        self.client.force_authenticate(user=self.user)
    
    def test_list_books(self):
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
