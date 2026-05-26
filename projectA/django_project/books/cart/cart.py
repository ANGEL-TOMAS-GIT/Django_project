from django.conf import settings
from books.models import Book
from decimal import Decimal

from django_project.settings import CART_SESSION_ID


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Book.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product
        for item in self.cart.values():
            item['total_price'] = Decimal(item['price']) * item['quantity']
            yield item

    def add(self, product: Book, override_quantity, quantity=1):
        product_id = str(product.pk)

        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.current_price)}
        if quantity <= 0:
            quantity = 1
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save_product()

    def remove(self, product: Book):
        product_id = str(product.pk)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save_product()

    def clear(self):
        del self.session[CART_SESSION_ID]
        self.save_product()

    def save_product(self):
        self.session.modified = True

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
