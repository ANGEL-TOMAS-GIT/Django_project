# from django.test import TestCase
# from django.contrib.auth import get_user_model
# from .models import Payment
#
# User = get_user_model()
#
# class PaymentModelTest(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(
#             username='payuser',
#             password='paypass123'
#         )
#
#     def test_create_payment(self):
#         payment = Payment.objects.create(
#             user=self.user,
#             amount=50.00,
#             status='pending'
#         )
#         self.assertEqual(payment.amount, 50.00)
#         self.assertEqual(payment.status, 'pending')
#
#     def test_payment_str(self):
#         payment = Payment.objects.create(
#             user=self.user,
#             amount=25.00,
#             status='completed'
#         )
#         self.assertIsNotNone(str(payment))
