from django.urls import path
from .views import (
    HomePageTemplateView,
    BooksListView,
    BookDetailView,
    BookCreateView,
    ManageBookListView,
    BookUpdateView,
    BookDeleteView,
    CartAddView,
    CartDetailView,
    CartRemoveView,
)

urlpatterns = [
    path('', HomePageTemplateView.as_view(), name="home"),
    path('books', BooksListView.as_view(), name="books"),
    path('books/<int:pk>/', BookDetailView.as_view(), name="book_detail"),
    path('create_book/', BookCreateView.as_view(), name="create_book"),
    path('manage_books/', ManageBookListView.as_view(), name="manage_books"),
    path('manage_book/<int:pk>/update_book/', BookUpdateView.as_view(), name="update_book"),
    path('manage_book/<int:pk>/delete_book/', BookDeleteView.as_view(), name="delete_book"),
    path('cart/', CartDetailView.as_view(), name="cart_detail"),
    path('cart/add/<int:pk>/', CartAddView.as_view(), name="cart_add"),
    path('cart/remove/<int:pk>/', CartRemoveView.as_view(), name="cart_remove"),
]
