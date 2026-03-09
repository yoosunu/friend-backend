import chromadb
from django.conf import settings


class ChromaService:
    def __init__(self):
        # 나중에 서버 모드로 바꿀 때 이 부분만 Client 설정으로 갈아끼우면 됩니다.
        self.client = chromadb.PersistentClient(path=settings.CHROMA_DB_PATH)
        self.collection = self.client.get_or_create_collection(name="notices")

    def upsert_notice(self, notice_id, text, metadata):
        self.collection.upsert(
            documents=[text], metadatas=[metadata], ids=[str(notice_id)]
        )

    def delete_notice(self, notice_id):
        self.collection.delete(ids=[str(notice_id)])

    def search(self, query_text, n_results=5):
        return self.collection.query(query_texts=[query_text], n_results=n_results)
