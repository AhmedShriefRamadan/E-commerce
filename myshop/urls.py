from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _

from payment import webhooks

# Alwayes place the more restricted urls first
urlpatterns = i18n_patterns(
    path("admin/", admin.site.urls),
    path(_('cart/'), include('cart.urls', namespace='cart')),
    path(_('orders/'), include('orders.urls', namespace='orders')),
    path(_('payment/'), include('payment.urls', namespace='payment')),
    path(_('coupons/'), include('coupons.urls',namespace='coupons')),
    path(_('rosetta/'), include('rosetta.urls')),
    path('', include('shop.urls',namespace='shop')),
)

# We have added the webhook URL pattern to urlpatterns outside of i18n_patterns() to ensure we maintain a single URL for Stripe event notifications.
urlpatterns += [
    path('webhook/', webhooks.stripe_webhook, name='stripe-webhook'),
]


# For Django to serve the uploaded media files using the development server
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                        document_root=settings.MEDIA_ROOT)
    

