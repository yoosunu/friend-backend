import chromadb
from django.conf import settings


class ChromaServiceNotice:
    def __init__(self):
        # gonna change when deploy (init client and save in file to alive data when server was shutted)
        self.client = chromadb.PersistentClient(path=settings.CHROMA_DB_PATH)
        self.collection = self.client.get_or_create_collection(name="notices")

    def upsert(self, id, text, metadata):
        self.collection.upsert(
            ids=[str(id)],
            documents=[text],  # real string
            metadatas=[metadata],  # json with detail
        )

    def delete(self, id):
        self.collection.delete(ids=[str(id)])

    def search(self, query_text, result_limit=10):
        return self.collection.query(query_texts=[query_text], n_results=result_limit)


chroma_service_notice = ChromaServiceNotice()
