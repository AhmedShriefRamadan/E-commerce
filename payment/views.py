from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from decimal import Decimal
import stripe
from django.conf import settings


from orders.models import Order



# create the Stripe instance
stripe.api_key = settings.STRIPE_SECRET_KEY


def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id =order_id)

    if request.method == 'POST':
        # We use request.build_absolute_uri() to generate an absolute URI from the URL path.
        success_url = request.build_absolute_uri(
            reverse('payment:completed')
        )
        cancel_url = request.build_absolute_uri(
            reverse('payment:canceled')
        )

        # Stripe checkout session data
        session_data = {
            'mode': 'payment',
            'client_reference_id': order.id,
            'success_url': success_url,
            'cancel_url': cancel_url,
            'line_items': []
        }

        for item in order.items.all():
            session_data['line_items'].append({
                'price_data': {
                    'unit_amount': int(item.price * Decimal('100')),
                    'currency':'usd',
                    'product_data': {
                        'name': item.product.name,
                    },
                },
                'quantity': item.quantity,
            })

        
        # stripe coupon
        if order.coupon:
            stripe_coupon = stripe.Coupon.create(
                name=order.coupon.code,
                percent_off=order.discount,
                duration='once'
            )
            session_data['discounts'] = [{
                'coupon':stripe_coupon.id
            }]

        # create Stripe checkout session
        session = stripe.checkout.Session.create(**session_data)

        # redirect to Stripe payment form
        # This status code is often used in situations where a form has been submitted, and the server is redirecting the client to a different resource or page after processing the form data. It helps prevent problems with resubmitting form data when refreshing a page.
        return redirect(session.url, code=303)
    else:
        return render(request, 'payment/process.html', locals())




def payment_completed(request):
    return render(request, 'payment/completed.html')


def payment_canceled(request):
    return render(request, 'payment/canceled.html')
