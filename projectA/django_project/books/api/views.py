from books.models import Book, Category
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import filters, viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate
from .serializers import BookSerializer, CategorySerializer, BookDetailSerializer
from books.api.utils import create_access_token, create_refresh_token
from django.conf import settings


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.filter(is_active=True, parent__isnull=True)
    serializer_class = CategorySerializer


class BookViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]

    search_fields = ['title', 'description']
    ordering_fields = ['price', 'title']
    lookup_field = 'slug'

    def get_queryset(self):
        qs = Book.active.all().select_related('category')

        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        if min_price:
            qs = qs.filter(price__gte=min_price)

        if max_price:
            qs = qs.filter(price__lte=max_price)

        return qs

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return BookDetailSerializer
        return BookSerializer


class GEtTokenPAirView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user = authenticate(
            email=request.data.get('email'),
            password=request.data.get('password')
        )
        if not user:
            return Response({'error': 'invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response({
            'access': create_access_token(user),
            'refresh': create_refresh_token(user)
        })


class RefreshTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        pass


# ============================================================
# ENDPOINTS FOR PROJECTB (WAREHOUSE) COMMUNICATION
# ============================================================


class CheckStockView(APIView):
    permission_classes = []  # No JWT required

    def get(self, request, product_id):
        # Check API Key
        api_key = request.headers.get('X-API-Key')
        if api_key != settings.WAREHOUSE_API_KEY:
            return Response({'error': 'Invalid API Key'}, status=401)

        try:
            book = Book.objects.get(id=product_id, is_active=True)
            return Response({
                'product_id': book.id,
                'sku': f'BOOK-{book.id}',
                'name': book.title,
                'available_quantity': book.stock,
                'price': float(book.price),
                'status': 'available' if book.stock > 0 else 'out_of_stock'
            })
        except Book.DoesNotExist:
            return Response({'error': 'Product not found'}, status=404)


class ReserveStockView(APIView):
    permission_classes = []

    def post(self, request, product_id):
        # Check API Key
        api_key = request.headers.get('X-API-Key')
        if api_key != settings.WAREHOUSE_API_KEY:
            return Response({'error': 'Invalid API Key'}, status=401)

        try:
            book = Book.objects.get(id=product_id, is_active=True)
            quantity = request.data.get('quantity', 0)
            order_id = request.data.get('order_id')

            if not quantity or quantity <= 0:
                return Response({
                    'error': 'Invalid quantity',
                    'quantity': quantity
                }, status=400)

            if book.stock >= quantity:
                book.stock -= quantity
                book.save()

                return Response({
                    'success': True,
                    'product_id': book.id,
                    'product_name': book.title,
                    'reserved_quantity': quantity,
                    'remaining_stock': book.stock,
                    'order_id': order_id
                }, status=200)
            else:
                return Response({
                    'success': False,
                    'error': 'Insufficient stock',
                    'available': book.stock,
                    'requested': quantity,
                    'product_id': product_id
                }, status=400)

        except Book.DoesNotExist:
            return Response({'error': 'Product not found'}, status=404)
