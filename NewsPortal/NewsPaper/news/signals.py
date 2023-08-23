from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import PostCategory
from .tasks import send_notifications


# @receiver(m2m_changed, sender=PostCategory)
# def weekly_notify(sender, instance, **kwargs):
#     if kwargs['action'] == 'post_add':
#         categories = instance.post_category.all()
#         subscribers: list[str] = []
#         for category in categories:
#             subscribers += category.subscribers.all()
#
#         subscribers_emails = [s.email for s in subscribers]
#
#         send_notifications(instance.preview(), instance.pk, instance.title, subscribers_emails)

