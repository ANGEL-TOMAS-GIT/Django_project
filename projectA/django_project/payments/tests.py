from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Payment


User = get_user_model()


def get_user_manager():
    return getattr(User, "objects", None) or getattr(User, "object")


class PaymentModelTest(TestCase):
    def setUp(self):
        self.user = get_user_manager().create_user(
            email='payuser@test.com',
            phone_number='2223334444',
            password='paypass123'
        )

    def test_create_payment(self):
        payment = Payment.objects.create(
            user=self.user,
            amount=50.00,
            status='pending'
        )

        self.assertEqual(payment.amount, 50.00)
        self.assertEqual(payment.status, 'pending')

    def test_payment_str(self):
        payment = Payment.objects.create(
            user=self.user,
            amount=25.00,
            status='completed'
        )

        self.assertIsNotNone(str(payment))

    def test_payment_status_default(self):
        payment = Payment.objects.create(
            user=self.user,
            amount=30.00
        )

        self.assertEqual(payment.status, 'pending')

    def test_payment_amount_positive(self):
            payment = Payment.objects.create(
                user=self.user,
                amount=10.00,
                status='pending'
            )
            self.assertGreater(payment.amount, 0)
