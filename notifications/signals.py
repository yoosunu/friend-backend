from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Notification
from .serviceChroma import chroma_service_notice


@receiver(post_save, sender=Notification)
def sync_notification_to_chroma(sender, instance, created, **kwargs):
    content = getattr(instance, "content", "") or ""
    embedding_text = f"{instance.title}\n{content[:500]}".strip()

    metadata = {
        "code": instance.code,
        "tag": instance.tag,
        "title": instance.title,
        "link": instance.link,
        "writer": instance.writer,
        "etc": instance.etc,
        "created_at": str(instance.created_at),
    }

    try:
        chroma_service_notice.upsert(
            id=str(instance.id), text=embedding_text, metadata=metadata
        )
    except Exception as e:
        import logging

        logger = logging.getLogger("django")
        logger.error(
            f"ChromaDB Sync Error: {e}",
            exc_info=True,
        )


@receiver(post_delete, sender=Notification)
def delete_notification_from_chroma(sender, instance, **kwargs):
    try:
        chroma_service_notice.delete(id=str(instance.id))
    except Exception as e:
        import logging

        logger = logging.getLogger("django")
        logger.error(
            f"ChromaDB Delete Error: {e}",
            exc_info=True,
        )
