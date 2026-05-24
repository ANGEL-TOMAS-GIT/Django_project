from rest_framework import serializers
from books.models import Category, Book


class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'parent', 'is_active', 'children']

    def get_children(self, obj):
        active_children = obj.children.filter(is_active=True)
        return CategorySerializer(active_children, many=True).data


class BookSerializer(serializers.ModelSerializer):
    current_price = serializers.DecimalField(
        max_digits=12, decimal_places=2, read_only=True
    )
    category_name = serializers.CharField(source='category', read_only=True)

    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'slug',
            'description',
            'price',
            'discount_price',
            'category',
            'stock',
            'is_active',
            'category_name',
            'current_price',
        ]


class BookDetailSerializer(serializers.ModelSerializer):
    current_price = serializers.DecimalField(
        max_digits=12, decimal_places=2, read_only=True
    )

    category = CategorySerializer(read_only=True)

    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'slug',
            'description',
            'price',
            'discount_price',
            'category',
            'stock',
            'is_active',
            'category_name',
            'current_price',
            'updated_at',
            'created_at'
        ]
