from django.test import TestCase
from django.contrib.auth import get_user_model


User = get_user_model()


def get_user_manager():
    return getattr(User, "objects", None) or getattr(User, "object")


class UserModelTest(TestCase):
    def test_create_user(self):
        user = get_user_manager().create_user(
            email='test@test.com',
            phone_number='1234567890',
            password='testpass123'
        )

        self.assertEqual(user.email, 'test@test.com')
        self.assertEqual(user.phone_number, '1234567890')
        self.assertTrue(user.check_password('testpass123'))

    def test_create_superuser(self):
        admin = get_user_manager().create_superuser(
            email='admin@test.com',
            phone_number='0987654321',
            password='admin123'
        )

        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.is_staff)
        self.assertEqual(admin.email, 'admin@test.com')

    def test_user_str(self):
        user = get_user_manager().create_user(
            email='str@test.com',
            phone_number='1112223333',
            password='strpass'
        )

        self.assertEqual(str(user), 'str@test.com')