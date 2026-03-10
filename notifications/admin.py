from django.contrib import admin
from .models import Notification
from .serviceChroma import chroma_service_notice


# Register your models here.
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "tag",
        "title",
        "link",
        "writer",
        "etc",
    )

    actions = ["sync_to_chroma_bulk", "sync_all_to_chroma"]

    @admin.action(description="sync to chromaDB that seleted")
    def sync_to_chroma_bulk(self, request, queryset):
        count = queryset.count()
        try:
            ids = [str(noti.id) for noti in queryset]
            documents = [
                f"{noti.title}\n{getattr(noti, 'content', '') or ''}".strip()
                for noti in queryset
            ]
            metadatas = [
                {
                    "code": noti.code,
                    "tag": noti.tag,
                    "title": noti.title,
                    "link": noti.link,
                    "writer": noti.writer,
                    "etc": noti.etc,
                    "created_at": str(noti.created_at),
                }
                for noti in queryset
            ]

            chroma_service_notice.collection.upsert(
                ids=ids, documents=documents, metadatas=metadatas
            )

            self.message_user(request, f"{count}개의 공지가 동기화되었습니다.")
        except Exception as e:
            self.message_user(request, f"오류 발생: {e}", level="error")

    @admin.action(description="⚠️ DB의 모든 공지 전체 동기화 (페이지 무관)")
    def sync_all_to_chroma(self, request, queryset):
        # queryset(선택된 것) 대신 Notification.objects.all()을 사용
        all_notis = Notification.objects.all()
        count = all_notis.count()

        try:
            ids = [str(obj.id) for obj in all_notis]
            # getattr로 'content' 에러 방어
            docs = [
                f"{obj.title}\n{getattr(obj, 'content', '') or ''}".strip()
                for obj in all_notis
            ]
            metas = [{"tag": obj.tag, "writer": obj.writer} for obj in all_notis]

            chroma_service_notice.collection.upsert(
                ids=ids, documents=docs, metadatas=metas
            )
            self.message_user(
                request, f"🚀 DB 전체 데이터 {count}개가 동기화되었습니다."
            )
        except Exception as e:
            self.message_user(request, f"❌ 에러 발생: {e}", level="error")
