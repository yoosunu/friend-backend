from django.core.management.base import BaseCommand
from notifications.models import Notification
from notifications.serviceChroma import ChromaServiceNotice


class Command(BaseCommand):
    help = "기존 PostgreSQL 데이터를 ChromaDB로 동기화합니다."

    def handle(self, *args, **options):
        chroma = ChromaServiceNotice()

        notifications = Notification.objects.all()
        total_count = notifications.count()

        self.stdout.write(f"총 {total_count}개의 데이터를 동기화 시작합니다...")

        for i, noti in enumerate(notifications, 1):
            metadata = {
                "code": noti.code,
                "tag": noti.tag,
                "title": noti.title,
                "link": noti.link,
                "writer": noti.writer,
                "etc": noti.etc,
                "created_at": str(noti.created_at),
            }

            chroma.upsert(
                id=noti.id,
                text=noti.title,
                metadata=metadata,
            )

            if i % 10 == 0:
                self.stdout.write(f"진행 중: {i}/{total_count}...")

        self.stdout.write(
            self.style.SUCCESS("동기화 완료! 이제 검색을 사용할 수 있습니다.")
        )
