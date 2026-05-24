from .models import Customer

from django.views.generic import View

from django.shortcuts import render, redirect
from books.orders.models import OrderItem
from books.cart.cart import Cart
from django.contrib import messages
from books.forms import OrderCreateForm
from books.tasks import send_confirmation_order_email


class OrderCreateView(View):
    template_name = "order/create_order.html"

    def get(self, request):
        cart = Cart(request)

        initial = {}

        if request.user.is_authenticated:
            user = request.user

            initial = {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
            }

            customer = hasattr(user, "customer")

            if customer:
                initial.update({
                    "phone": getattr(customer, "phone", ""),
                    "address": getattr(customer, "address", "")
                })

        form = OrderCreateForm(initial=initial)

        context = {
            "form": form,
            "cart": cart,
            "total_price": cart.get_total_price()
        }

        return render(request, self.template_name, context)

    def post(self, request):
        cart = Cart(request)

        if not cart.cart:
            messages.warning(request, "The Cart is Empty!!")
            return redirect("cart_detail")

        form = OrderCreateForm(request.POST)

        if form.is_valid():
            order = form.save(commit=False)
            order.total_price = cart.get_total_price()

            if request.user.is_authenticated:
                customer, _ = Customer.objects.get_or_create(user=request.user)
                order.customer = customer

            order.save()

            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    price=item["price"],
                    quantity=item["quantity"]
                )

            cart.clear()

            messages.success(
                request,
                f"The Order #{order.id} successfully completed"
            )
            send_confirmation_order_email.delay(order.id)
            return redirect('payments:checkout_order', order_id=order.id)

        context = {
            "form": form,
            "cart": cart,
            "total_price": cart.get_total_price()
        }

        return render(request, self.template_name, context)
