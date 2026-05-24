import time
from celery import shared_task
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session
from django.core.mail import send_mail
from django.conf import settings

from books.orders.models import Order

User = get_user_model()


@shared_task
def test_task(user_id: int | None):
    user = None
    if user_id:
        user = User.objects.filter(id=user_id).first()
    requested_user: AbstractBaseUser | str = user or 'Not authenticated User'
    return f'Task executed successfully! Requested by: {requested_user}'


@shared_task
def send_confirmation_order_email(order_id: int):
    try:
        order = Order.objects.prefetch_related('items__product').get(pk=order_id)

    except Order.DoesNotExist:
        return f'Order # {order_id} not found'
    items_text = '\n'.join(
        f' * {item.product.title} x {item.quantity} = {item.get_total} EUR'
        for item in order.items.all()
    )

    subject = f'Order #{order_id} confirmed!'

    body = {
        f'Dear {order.first_name} \n\n'
        f'Thanks for order #{order_id} \n'
        f'Items: \n{items_text}\n'
        f'Total: {order.total_price}'
    }
    try:
        send_mail(
            subject=subject,
            message=body,
            recipient_list=[order.email],
            from_email=settings.DEFAULT_EMAIL_FROM
        )
    except Exception as e:
        return f'Email failed for order {order_id} {e}'
    return f'Email sent to {order.email}'


@shared_task
def generate_report():
    time.sleep(10)
    print("Report generated")


@shared_task
def clear_expired_sessions():
    Session.objects.filter(expire_date__lt=None).delete()
    print("Expired sessions cleared")
