from django.contrib import admin
from .models import Book, Category, Customer
from django.contrib.auth.models import Permission
from books.orders.models import Order, OrderItem


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    pass


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "book_author", "author", "created_at", "price", "stock", "is_active", "description")
    list_filter = ("author", "created_at")
    search_fields = ("title",)
    ordering = ("author",)


class BookInline(admin.TabularInline):
    model = Book
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [BookInline]


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "price", "quantity")
    list_filter = ("order",)
    search_fields = ("order",)
    ordering = ("order",)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
