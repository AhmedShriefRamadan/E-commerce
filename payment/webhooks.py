import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from orders.models import Order
from . tasks import payment_completed
from shop.recommender import Recommender



# The @csrf_exempt decorator is used to prevent Django from performing the CSRF validation that is done by default for all POST requests
@csrf_exempt
def stripe_webhook(request):
    payload = request.body

    # In Django, request.META is a dictionary containing all available HTTP headers. It provides metadata about the request being made to a Django view. This dictionary includes information like the client's IP address, user agent, requested URL, and other details related to the HTTP request.
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']

    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)
    
    if event.type == 'checkout.session.completed' :
        session = event.data.object
        if session.mode == 'payment' and session.payment_status == 'paid':
            try:
                order = Order.objects.get(id=session.client_reference_id)
            except Order.DoesNotExist:
                return HttpResponse(status=404)
            
            order.paid = True
            order.stripe_id = session.payment_intent
            order.save()
            products =[]
            for p in order.items.select_related('product').all():
                products.append(p.product)
            r = Recommender()
            r.products_bought(products)

            # Launch asynchronous task
            payment_completed.delay(order.id)

    return HttpResponse(status=200)