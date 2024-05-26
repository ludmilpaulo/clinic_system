from datetime import datetime
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Order
from .utils import send_order_email

@receiver(pre_save, sender=Order)
def track_order_status_change(sender, instance, **kwargs):
    if instance.pk:
        # Retrieve the previous state of the object
        previous = Order.objects.get(pk=instance.pk)
        instance._previous_status = previous.status

@receiver(post_save, sender=Order)
def order_status_changed(sender, instance, **kwargs):
    if hasattr(instance, '_previous_status') and instance._previous_status != instance.status:
        context = {
            'username': instance.user.username,
            'order_id': instance.id,
            'status': instance.status,
            'total_price': instance.total_price,
            'year': datetime.now().year
        }
        send_order_email(
            subject='Order Status Update',
            template_name='order_status_update_email.html',  # Path to your email template
            context=context,
            recipient_list=[instance.user.email]
        )
