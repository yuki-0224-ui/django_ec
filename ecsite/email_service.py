from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


def send_order_confirmation(order):
    if not order.email:
        return

    context = {
        'order': order,
        'order_items': order.items.select_related('product').all(),
    }

    subject = f'【ご注文確認】注文番号: {order.id}'
    html_message = render_to_string(
        'ecsite/emails/order_confirmation.html', context)

    send_mail(
        subject=subject,
        message='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[order.email],
        html_message=html_message,
        fail_silently=False,
    )
