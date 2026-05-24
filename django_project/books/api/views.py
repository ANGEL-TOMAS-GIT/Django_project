from books.models import Book, Category
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import filters, viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate
from .serializers import BookSerializer, CategorySerializer, BookDetailSerializer
from books.api.utils import create_access_token, create_refresh_token


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
