# from django.test import TestCase
# from django.contrib.auth import get_user_model
#
# User = get_user_model()
#
# class UserModelTest(TestCase):
#     def test_create_user(self):
#         user = User.objects.create_user(
#             username='testuser',
#             email='test@test.com',
#             password='testpass123'
#         )
#         self.assertEqual(user.username, 'testuser')
#         self.assertTrue(user.check_password('testpass123'))
#
#     def test_create_superuser(self):
#         admin = User.objects.create_superuser(
#             username='admin',
#             email='admin@test.com',
#             password='admin123'
#         )
#         self.assertTrue(admin.is_superuser)
#         self.assertTrue(admin.is_staff)
#
#     def test_user_str(self):
#         user = User.objects.create_user(
#             username='struser',
#             email='str@test.com',
#             password='strpass'
#         )
#         self.assertEqual(str(user), 'struser')
