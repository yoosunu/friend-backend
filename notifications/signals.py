from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Notification


@receiver(pre_save, sender=Notification)
def check_and_delete_old_records(sender, instance, **kwargs):
    max_records = 50
    total_records = sender.objects.count()
    if total_records > max_records:
        excess_records = total_records - max_records + 1
        sender.objects.order_by("code")[:excess_records].delete()
