from rest_framework.views import APIView
from rest_framework.response import Response
from books.cart.cart import Cart
from .serializers import CartSerializer


class CartAPIView(APIView):

    def get(self, request):
        cart = Cart(request)

        items = []
        for item in cart:
            items.append({
                "title": item["product"].title,
                "quantity": item["quantity"],
                "price": item["price"],
                "total_price": item["total_price"],
            })

        serializer = CartSerializer({
            "items": items,
            "total": cart.get_total_price()
        })

        return Response(serializer.data)
