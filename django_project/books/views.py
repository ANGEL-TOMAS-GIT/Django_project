from .models import Book
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import (
    ListView,
    TemplateView,
    CreateView,
    UpdateView,
    DeleteView,
    View
)
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from books.cart.cart import Cart
from django.contrib import messages
from asgiref.sync import sync_to_async


class HomePageTemplateView(TemplateView):
    template_name = "index.html"


class BaseBooksListView(ListView):
    model = Book
    context_object_name = "books"

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get("q")

        if query:
            qs = qs.filter(
                Q(name__icontains=query) |
                Q(book_author__icontains=query) |
                Q(category__name__icontains=query)
            )
        return qs


class BooksListView(BaseBooksListView):
    template_name = "book_list.html"


class ManageBookListView(BaseBooksListView):
    template_name = "manage_books.html"


class BookDetailView(View):
    template_name = "book_description.html"

    async def get(self, request, pk):
        try:
            book = await Book.objects.aget(pk=pk)
        except Book.DoesNotExist:
            raise Http404("Book not found")

        return render(request, self.template_name, {"book": book})


class BookCreateView(PermissionRequiredMixin, CreateView):
    model = Book
    fields = "__all__"
    template_name = "book_create.html"
    permission_required = 'books.add_book'
    raise_exception = True

    def get_success_url(self):
        return reverse_lazy('books')


class BookUpdateView(PermissionRequiredMixin, UpdateView):
    model = Book
    fields = "__all__"
    template_name_suffix = "_update_form"
    template_name = "book_update.html"
    permission_required = 'books.update_book'
    raise_exception = True

    def get_success_url(self):
        return reverse_lazy('books')


class BookDeleteView(PermissionRequiredMixin, DeleteView):
    model = Book
    template_name = "book_delete.html"
    permission_required = 'books.delete_book'
    raise_exception = True

    success_url = reverse_lazy('books')


class CartDetailView(TemplateView):
    template_name = "cart/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart(self.request)

        context["cart"] = cart
        context["total_price"] = cart.get_total_price()
        return context


class CartAddView(View):

    async def post(self, request, pk):
        product = await Book.objects.aget(
            pk=pk,
            is_active=True
        )

        cart = await sync_to_async(Cart)(request)

        quantity = int(request.POST.get("quantity", 1))

        await sync_to_async(cart.add)(
            product=product,
            quantity=quantity,
            override_quantity=True
        )

        await sync_to_async(messages.success)(
            request,
            f"{product.title} added to cart"
        )

        return redirect("cart_detail")


class CartRemoveView(View):

    def get(self, request, pk):
        cart = Cart(request)
        product = get_object_or_404(Book, pk=pk, is_active=True)
        cart.remove(product)
        messages.info(request, f'{product.title} removed from the cart')
        return redirect("cart_detail")
