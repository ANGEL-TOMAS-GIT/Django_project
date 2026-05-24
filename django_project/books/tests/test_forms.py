from django.test import TestCase

from books.forms import OrderCreateForm


class TestForm(TestCase):
    def test_order_form_valid(self):
        form = OrderCreateForm(data={
            "first_name": "Angel",
            "last_name": "G",
            "email": "a@test.com",
            "phone": "123456",
            "address": "Berlin"
        })
        assert form.is_valid()

    def test_order_form_invalid(self):
        form = OrderCreateForm(data={})
        assert not form.is_valid()
